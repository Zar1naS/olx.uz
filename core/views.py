from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from ads.models import Ad, Category, Location


def home_view(request):
    """Home page view"""
    # Get search parameters
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    location_slug = request.GET.get('location', '')
    
    # Filter ads
    ads = Ad.objects.filter(is_active=True).select_related('category', 'location', 'user')
    
    if query:
        ads = ads.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_slug:
        ads = ads.filter(category__slug=category_slug)
    
    if location_slug:
        ads = ads.filter(location__slug=location_slug)
    
    # Order by featured/vip first, then by creation date
    ads = ads.order_by('-is_featured', '-is_vip', '-created_at')
    
    # Pagination
    paginator = Paginator(ads, 12)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    
    # Get categories and locations for filters
    categories = Category.objects.filter(is_active=True)
    locations = Location.objects.filter(is_active=True)
    
    context = {
        'ads': ads,
        'categories': categories,
        'locations': locations,
        'current_query': query,
        'current_category': category_slug,
        'current_location': location_slug,
        'total_ads': Ad.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'core/home.html', context)
