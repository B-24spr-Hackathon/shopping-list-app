from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


"""
HealthcheckView
ALBのヘルスチェックに対応するView
"""
class HealthcheckView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK)