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
from shop.serializers.apply import OwnListsSerializer
class ApplyView(APIView):

    # リストオーナー情報取得 GET
    def get(self, request, user_id):
        # リストオーナーを取得
        owner = get_object_or_404(User, pk=user_id)

        # 取得したオーナーに紐づくリストを取得
        lists = List.objects.filter(owner_id=user_id)
        serializer = OwnListsSerializer(lists, many=True)

        response_data = {
            'user_id': user_id,
            'user_name': owner.user_name,
            'user_icon': owner.user_icon,
            'lists': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)