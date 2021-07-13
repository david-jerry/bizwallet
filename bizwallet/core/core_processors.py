from .models import Services

def all_services(request):
    return {'all_services':Services.objects.all().filter(active=True)}