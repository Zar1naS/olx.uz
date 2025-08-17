from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from .models import Ad, Category, Location, AdReport, AdImage
from .forms import AdForm, AdImageFormSet, AdSearchForm


def ads_list_view(request):
    """List all ads with filters"""
    ads = Ad.objects.filter(is_active=True).select_related('category', 'location', 'user')
    
    # Apply filters
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')
    
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if category:
        ads = ads.filter(category__slug=category)
        
    if location:
        ads = ads.filter(location__slug=location)
    
    # Order by featured/vip first
    ads = ads.order_by('-is_featured', '-is_vip', '-created_at')
    
    # Pagination
    paginator = Paginator(ads, 12)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    
    context = {
        'ads': ads,
        'categories': Category.objects.filter(is_active=True),
        'locations': Location.objects.filter(is_active=True),
        'current_query': query,
        'current_category': category,
        'current_location': location,
    }
    
    return render(request, 'ads/list.html', context)


def ad_detail_view(request, slug):
    """Ad detail view"""
    ad = get_object_or_404(Ad, slug=slug, is_active=True)
    
    # Increment views count (but not for the owner)
    if request.user != ad.user:
        ad.increment_views()
    
    # Check if current user has favorited this ad
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = ad.favorited_by.filter(id=request.user.id).exists()
    
    # Get related ads
    related_ads = Ad.objects.filter(
        category=ad.category,
        is_active=True
    ).exclude(id=ad.id)[:6]
    
    context = {
        'ad': ad,
        'is_favorite': is_favorite,
        'related_ads': related_ads,
        'is_owner': request.user == ad.user,
    }
    
    return render(request, 'ads/detail.html', context)


def category_view(request, slug):
    """Category page view with location and price filtering"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    ads = category.ads.filter(is_active=True)
    
    # Apply search filter
    query = request.GET.get('q')
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    # Apply location filter if provided
    location_slug = request.GET.get('location')
    selected_location = None
    if location_slug:
        try:
            selected_location = Location.objects.get(slug=location_slug, is_active=True)
            ads = ads.filter(location=selected_location)
        except Location.DoesNotExist:
            pass
    
    # Apply price filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            ads = ads.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            ads = ads.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Order ads
    ads = ads.order_by('-is_featured', '-is_vip', '-created_at')
    
    # Pagination
    paginator = Paginator(ads, 12)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    
    context = {
        'category': category,
        'ads': ads,
        'locations': Location.objects.filter(is_active=True),
        'selected_location': selected_location,
        'current_location': location_slug,
    }
    
    return render(request, 'ads/category.html', context)


def location_view(request, slug):
    """Location page view"""
    location = get_object_or_404(Location, slug=slug, is_active=True)
    ads = location.ads.filter(is_active=True).order_by('-is_featured', '-is_vip', '-created_at')
    
    # Pagination
    paginator = Paginator(ads, 12)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    
    context = {
        'location': location,
        'ads': ads,
        'categories': Category.objects.filter(is_active=True),
    }
    
    return render(request, 'ads/location.html', context)


@login_required
def create_ad_view(request):
    """Create new ad with image upload"""
    if request.method == 'POST':
        form = AdForm(request.POST)
        image_formset = AdImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                # Create the ad
                ad = form.save(commit=False)
                ad.user = request.user
                ad.save()
                
                # Save images
                images = image_formset.save(commit=False)
                for image in images:
                    if image.image:  # Only save if image is provided
                        image.ad = ad
                        image.save()
                
                # If no main image is selected, make the first image main
                if not ad.images.filter(is_main=True).exists() and ad.images.exists():
                    first_image = ad.images.first()
                    first_image.is_main = True
                    first_image.save()
                
                messages.success(request, _('E\'lon muvaffaqiyatli yaratildi!'))
                return redirect('ads:detail', slug=ad.slug)
    else:
        form = AdForm()
        image_formset = AdImageFormSet()
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'categories': Category.objects.filter(is_active=True),
        'locations': Location.objects.filter(is_active=True),
    }
    
    return render(request, 'ads/create.html', context)


@login_required
def edit_ad_view(request, slug):
    """Edit existing ad"""
    ad = get_object_or_404(Ad, slug=slug, user=request.user)
    
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        image_formset = AdImageFormSet(request.POST, request.FILES, instance=ad)
        
        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                # Update the ad
                updated_ad = form.save()
                
                # Save images
                image_formset.save()
                
                # If no main image is selected, make the first image main
                if not updated_ad.images.filter(is_main=True).exists() and updated_ad.images.exists():
                    first_image = updated_ad.images.first()
                    first_image.is_main = True
                    first_image.save()
                
                messages.success(request, _('E\'lon muvaffaqiyatli yangilandi!'))
                return redirect('ads:detail', slug=updated_ad.slug)
    else:
        form = AdForm(instance=ad)
        image_formset = AdImageFormSet(instance=ad)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'ad': ad,
        'categories': Category.objects.filter(is_active=True),
        'locations': Location.objects.filter(is_active=True),
    }
    
    return render(request, 'ads/edit.html', context)


@login_required
def delete_ad_view(request, slug):
    """Delete ad"""
    ad = get_object_or_404(Ad, slug=slug, user=request.user)
    
    if request.method == 'POST':
        ad_title = ad.title  # Store the title before deactivating
        ad.is_active = False
        ad.save()
        messages.success(request, _('Mahsulot o\'chirildi!'))
        return redirect('users:my_ads')
    
    return render(request, 'ads/delete.html', {'ad': ad})




@login_required
@require_POST
def ajax_delete_ad(request):
    """AJAX delete ad endpoint"""
    ad_id = request.POST.get('ad_id')
    
    if not ad_id:
        return JsonResponse({'error': 'Ad ID required'}, status=400)
    
    try:
        ad = get_object_or_404(Ad, id=ad_id, user=request.user)
        ad_title = ad.title
        ad.is_active = False
        ad.save()
        return JsonResponse({
            'success': True, 
            'message': _('Mahsulot o\'chirildi!')
        })
    except Ad.DoesNotExist:
        return JsonResponse({'error': 'Ad not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def report_ad_view(request):
    """Report inappropriate ad"""
    ad_id = request.POST.get('ad_id')
    reason = request.POST.get('reason')
    description = request.POST.get('description', '')
    
    if not ad_id or not reason:
        return JsonResponse({'error': 'Required fields missing'}, status=400)
    
    try:
        ad = Ad.objects.get(id=ad_id)
        report, created = AdReport.objects.get_or_create(
            ad=ad,
            user=request.user,
            defaults={
                'reason': reason,
                'description': description
            }
        )
        
        if created:
            return JsonResponse({'message': str(_('Shikoyat yuborildi'))})
        else:
            return JsonResponse({'message': str(_('Siz allaqachon shikoyat yuborgansiz'))})
            
    except Ad.DoesNotExist:
        return JsonResponse({'error': 'Ad not found'}, status=404)
