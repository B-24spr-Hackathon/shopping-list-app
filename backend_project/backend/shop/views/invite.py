from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import List, Member, User
from shop.authentication import CustomJWTAuthentication
from shop.serializers.invite import FindUserSerializer
from django.shortcuts import get_object_or_404
from shop.permissions import IsOwner

class InviteView(APIView):
    # JWT認証を要求、オーナーのみ許可
    permission_classes = [IsAuthenticated, IsOwner]
    # GETメソッドだけは誰でも可
    def get_permissions(self):
       if self.request.method == 'GET':
           return [IsAuthenticated()] 
       return [IsAuthenticated(), IsOwner()]
    
    # 招待処理　招待者情報取得 GET
    def get(self, request, user_id):
        # 招待者を取得
        invitee = get_object_or_404(User, pk=user_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request,invitee)
        invitee_data = FindUserSerializer(invitee).data

        return Response(invitee_data, status=status.HTTP_200_OK)

    # 招待処理　招待送信　POST
    def post(self, request)
        


    
