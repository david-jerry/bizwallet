from .models import Services
from bizwallet.users.models import User

def all_services(request):
    return {'all_services':Services.objects.filter(active=True)}

def all_users(request):
    return {'all_users':User.objects.filter(is_active=True).count()}

def all_field_users(request):
    return {'all_field_users':User.objects.filter(is_active=True, is_field_worker=True).count()}