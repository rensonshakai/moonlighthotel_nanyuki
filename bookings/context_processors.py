from .models import SiteSetting

def site_settings(request):
    # Fetch the first (and only) settings object. If it doesn't exist, return an empty dict.
    settings = SiteSetting.objects.first()
    return {
        'site_settings': settings
    }