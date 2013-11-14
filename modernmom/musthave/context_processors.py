from django.contrib.sites.models import Site

def site(request):
    return {
        'site': Site.objects.get_current(),
        'site_next': 'http://%s%s' % (Site.objects.get_current(),request.get_full_path())
        }
