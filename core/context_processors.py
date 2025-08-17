from django.conf import settings


def site_settings(request):
    """Add common site settings to context"""
    return {
        'SITE_NAME': 'OLX.uz',
        'SITE_DESCRIPTION': 'Uzbekistondagi eng katta elon taxtasi',
        'SITE_KEYWORDS': 'elonlar, sotish, sotib olish, uzbekistan, olx',
    }
