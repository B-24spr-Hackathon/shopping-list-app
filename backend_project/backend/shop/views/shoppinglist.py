from django.shortcuts import get_object_or_404
from rest_framework import status
from shop.models import Item, List, Member
from shop.serializers.shoppinglist import ShoppingListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from shop.permissions import IsOwnerOrInvitee
import calendar
from datetime import datetime


# 買い物リスト表示(GET)
class ShoppingListView(APIView):
    # JWT認証を要求、オーナーまたは招待者のみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrInvitee] 

    def get(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # リストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id, to_list=True)
        serializer = ShoppingListSerializer(items, many=True)
        # authorityの値を取得(オーナーの場合は自動的にTrue)
        if list_instance.owner_id == request.user:
            authority = True
        else:
            member = Member.objects.filter(list_id=list_id, invitee_id=request.user).first()
            authority = member.authority

        # 買い物予定日
        next_shopping_day = self.calculate_next_shopping_day(list_instance.shopping_day)

        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'next_shopping_day': next_shopping_day.strftime('%Y-%m-%d'),
            'authority': authority,
            'items': serializer.data
        }
        return Response(response_data)
    

    # 買い物予定日の計算
    def calculate_next_shopping_day(self, shopping_day):
        today = datetime.today()
        current_year = today.year
        current_month = today.month

        # 今月の最終日を取得
        _, last_day_this_month = calendar.monthrange(current_year, current_month)
        adjusted_day_this_month = min(shopping_day, last_day_this_month)
        shopping_date_this_month = datetime(current_year, current_month, adjusted_day_this_month)
        shopping_date_this_month = datetime(current_year, current_month, shopping_day)

        if today <= shopping_date_this_month:
            return shopping_date_this_month
        else:
            next_month = current_month + 1 if current_month < 12 else 1
            next_year = current_year if current_month < 12 else current_year + 1
            _, last_day_next_month = calendar.monthrange(next_year, next_month)
            adjusted_day_next_month = min(shopping_day, last_day_next_month)

            return datetime(next_year, next_month, adjusted_day_next_month)
        



    
