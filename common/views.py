from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return JsonResponse({"status": "ok"})
