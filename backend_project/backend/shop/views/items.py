from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from shop.models import Item, List
from shop.serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shop.permissions import IsOwnerOrGuestWithAuthority
from datetime import date
import logging

logger = logging.getLogger("backend")


class ItemCreateView(APIView):
    # JWT認証を要求、オーナーまたは編集権限を持つゲストのみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrGuestWithAuthority]

    # アイテムリスト表示
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
        # 取得したリストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id)
        serializer = ItemSerializer(items, many=True)
        # レスポンスをカスタマイズ
        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'items': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # アイテム新規作成
    def post(self, request, list_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        # リストを取得
        try:
            list_instance = get_object_or_404(List, pk=list_id)
        except Http404:
            logger.error("リストが存在しない")
            return Response({"error": "リストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)
        
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        serializer = ItemCreateSerializer(data=request.data)
        # list_idを使ってListインスタンスを取得し、アイテムを保存
        if serializer.is_valid():
            serializer.save(list_id=list_instance)
            # 作成、保存されたアイテムをシリアライズして返す
            response_serializer = ItemResponseSerializer(serializer.instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"{serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    # JWT認証を要求、オーナーまたは編集権限を持つゲストのみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrGuestWithAuthority]

    # アイテム更新
    def patch(self, request, list_id, item_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        # リストを取得
        try:
            list_instance = get_object_or_404(List, pk=list_id)
        except Http404:
            logger.error("リストが存在しない")
            return Response({"error": "リストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)

        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)

        # アイテムのインスタンスを取得
        try:
            item_instance = get_object_or_404(Item, pk=item_id)
        except Http404:
            logger.error("アイテムが存在しない")
            return Response({"error": "アイテムが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ItemUpdateSerializer(item_instance, data=request.data, context={"request": request}, partial=True)

        if serializer.is_valid():
            # 更新前の直近開封日とto_listを保存
            previous_last_open_at = item_instance.last_open_at
            previous_to_list = item_instance.to_list
            # データを更新して保存
            to_list = request.data.get('to_list', item_instance.to_list)
            serializer.save(to_list=to_list)

            # to_listがfalseからtrueに更新されたらlast_open_atを更新する
            if to_list == True and previous_to_list == False:
                item_instance.last_open_at = date.today()
                list_instance.save()

                # 頻度が短くなっていれば、消費サイクルを更新
                cycle = item_instance.consume_cycle
                last_open_at = previous_last_open_at
                new_cycle = CheckCycle(cycle, last_open_at)
                
                if new_cycle is not False:
                    item_instance.consume_cycle = new_cycle
                    item_instance.save()

            # 更新されたフィールドのみ辞書として取得
            update_fields = {field: request.data[field] for field in request.data}
            # 更新されたフィールドのみをレスポンスとして返す
            return Response(update_fields, status=status.HTTP_200_OK)
        else:
            logger.error(f"{serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # アイテム削除
    def delete(self, request, list_id, item_id):
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
        # アイテムのインスタンスを取得
        try:
            item_instance = get_object_or_404(Item, pk=item_id)
        except Http404:
            logger.error("アイテムが存在しない")
            return Response({"error": "アイテムが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)

        response_serializer = ItemResponseSerializer(item_instance)
        serialized_data = response_serializer.data

        item_instance.delete()
        # 削除したアイテムのデータを表示する
        return Response(serialized_data, status=status.HTTP_200_OK)


def CheckCycle(cycle, last_open_at):
    today = timezone.now().date()
    # 今日-最終開封日の差をint型で取得
    new_cycle = (today - last_open_at).days

    # 消費頻度が設定よりも短い場合は新しい消費頻度を返す
    if new_cycle < cycle:
        return new_cycle

    # 消費頻度が設定よりも長い場合はFalseを返す
    else:
        return False