from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return Response({"status": "ok"})
