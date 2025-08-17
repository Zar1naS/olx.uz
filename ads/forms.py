from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import Ad, AdImage, Category, Location


class AdForm(forms.ModelForm):
    """Form for creating and editing ads"""
    
    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'location', 'price', 'condition', 'phone', 'is_negotiable']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('E\'lon sarlavhasi'),
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('E\'lon haqida batafsil ma\'lumot'),
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'location': forms.Select(attrs={
                'class': 'form-select modern-select location-select',
                'required': True,
                'data-placeholder': 'Joylashuvni tanlang...',
                'data-search': 'true'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Narx (so\'m)'),
                'min': 0
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('+998XXXXXXXXX')
            }),
            'is_negotiable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for active categories and locations
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['location'].queryset = Location.objects.filter(is_active=True).order_by('order', 'name')
        
        # Set empty labels
        self.fields['category'].empty_label = _('Kategoriyani tanlang')
        self.fields['location'].empty_label = _('Joylashuvni tanlang')
        
        # Mark required fields
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['category'].required = True
        self.fields['location'].required = True
        self.fields['price'].required = True
        self.fields['phone'].required = True

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError(_('Narx noldan katta bo\'lishi kerak'))
        return price

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic phone validation for Uzbekistan numbers
            import re
            if not re.match(r'^\+?998[0-9]{9}$', phone.replace(' ', '').replace('-', '')):
                raise forms.ValidationError(_('Telefon raqam noto\'g\'ri formatda. Masalan: +998901234567'))
        return phone


class AdImageForm(forms.ModelForm):
    """Form for ad images"""
    
    class Meta:
        model = AdImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# Create formset for multiple images
AdImageFormSet = inlineformset_factory(
    Ad, 
    AdImage,
    form=AdImageForm,
    fields=['image', 'is_main'],
    extra=5,  # Show 5 empty forms by default
    max_num=10,  # Maximum 10 images per ad
    can_delete=True,
    validate_max=True,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        'is_main': forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    }
)


class AdSearchForm(forms.Form):
    """Form for searching ads"""
    
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Qidirish...'),
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True).order_by('order', 'name'),
        required=False,
        empty_label=_('Barcha kategoriyalar'),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True).order_by('order', 'name'),
        required=False,
        empty_label=_('Barcha viloyatlar'),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    min_price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Minimal narx'),
            'min': 0
        })
    )
    max_price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Maksimal narx'),
            'min': 0
        })
    )
