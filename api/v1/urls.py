from django.urls import path, include
from django.http import JsonResponse
urlpatterns = [
    path('', include('apps.accounts.urls')),        # API key management
    path('', include('apps.domains.urls')),         # Domain management
    # Future: templates, messages, etc.
]

app_name = 'api'

def domains_api(request):
    return JsonResponse({"message": "Domains endpoint placeholder"})

urlpatterns = [
    path('domains/', domains_api, name='domains'),
]