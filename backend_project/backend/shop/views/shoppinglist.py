from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from shop.models import Item, List, Member
from shop.serializers.shoppinglist import ShoppingListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shop.permissions import IsOwnerOrGuest
import calendar
from datetime import date
import logging

logger = logging.getLogger("backend")


# 買い物リスト表示(GET)
class ShoppingListView(APIView):
    # JWT認証を要求、オーナーまたはゲストのみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrGuest] 

    def get(self, request, list_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        # リストを取得
        try:
            list_instance = get_object_or_404(List, pk=list_id)
        except Http404:
            logger.error("リストが存在しない")
            return Response({"error": "リストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)
        
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # リストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id, to_list=True)
        serializer = ShoppingListSerializer(items, many=True)
        # authorityの値を取得(オーナーの場合は自動的にTrue)
        if list_instance.owner_id == request.user:
            authority = True
        else:
            member = Member.objects.filter(list_id=list_id, guest_id=request.user).first()
            authority = member.authority

        # 買い物予定日
        next_shopping_day = self.calculate_next_shopping_day(list_instance.shopping_day)

        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'next_shopping_day': next_shopping_day,
            'authority': authority,
            'items': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # 買い物予定日の計算
    def calculate_next_shopping_day(self, shopping_day):
        if shopping_day in [None, '', 'null'] :
            logger.info("買い物日未設定")
            return "買い物日は設定されていません"

        today = date.today()
        current_year = today.year
        current_month = today.month

        # 今月の最終日を取得
        _, last_day_this_month = calendar.monthrange(current_year, current_month)
        adjusted_day_this_month = min(shopping_day, last_day_this_month)
        shopping_date_this_month = date(current_year, current_month, adjusted_day_this_month)

        if today <= shopping_date_this_month:
            logger.info("今月の買い物日")
            return shopping_date_this_month
        else:
            next_month = current_month + 1 if current_month < 12 else 1
            next_year = current_year if current_month < 12 else current_year + 1
            _, last_day_next_month = calendar.monthrange(next_year, next_month)
            adjusted_day_next_month = min(shopping_day, last_day_next_month)

            logger.info("来月の買い物日")
            return date(next_year, next_month, adjusted_day_next_month)
