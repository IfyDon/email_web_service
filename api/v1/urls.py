from django.urls import path, include
from django.http import JsonResponse
urlpatterns = [
    path('', include('apps.accounts.urls')),        # API key management
    path('', include('apps.domains.urls')),         # Domain management
    # Future: templates, messages, etc.
]

app_name = 'api'

# Placeholder views
def domains_api(request):
    return JsonResponse({"message": "Domains endpoint placeholder"})

def verify_domain(request, domain_id):
    # domain_id is captured from the URL
    return JsonResponse({
        "message": f"Verification endpoint for domain ID {domain_id} (placeholder)"
    })

urlpatterns = [
    path('domains/', domains_api, name='domains'),
    path('domains/<int:domain_id>/verify/', verify_domain, name='domain-verify'),
]