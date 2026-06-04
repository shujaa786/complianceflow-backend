from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "ComplianceFlow API",
        "version": "1.0.0"
    })