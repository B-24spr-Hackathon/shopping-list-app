from django.shortcuts import render
from rest_framework import, status
from ..models import Item, List
from ..serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


# アイテムリスト表示および新規作成
class ItemView(APIView):

    def get(self, request, user_id, list_id):
        # owner または invitee, かつ list_idでフィルタリング
        items = Item.objects.filter(
            (Q(list_id__owner_id=user_id) | 
            Q(list_id__members__invitee_id=user_id)) & 
            Q(list_id=list_id)
        ) 
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    


    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

   # リクエストメソッドにより、シリアライザー設定
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ItemCreateSerializer
        return ItemSerializer    
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        list_id = self.kwargs.get('list_id')

        # (owner または invitee) かつ list_id__id=list_id の条件でフィルタリング
        return Item.objects.filter(
            Q(list_id__owner_id=user_id) | 
            Q(list_id__members__invitee_id=user_id),
            list_id=list_id
        ) 
    # urlからlist_id を取得してPost
    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id')
        list_instance = List.objects.get(pk=list_id) 
        serializer.save(list_id=list_instance)

    # POSTへのレスポンス項目をカスタマイズ
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # レスポンス表示に利用するserializer設定
        retrieve_serializer = ItemResponseSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# アイテムの更新
class ItemUpdate(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = 'item_id'

    # リクエストメソッドから動的にserializerを選択
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ItemUpdateSerializer
        return ItemResponseSerializer

    # (owner または invitee) かつ item_id=item_id の条件でフィルタリング
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Item.objects.filter(
            Q(list_id__owner_id=user_id) | 
            Q(list_id__members__invitee_id=user_id)
        )  
    
    def patch(self, request, *args, **kwargs):
        item = self.get_object() # 既存のアイテムを取得
        serializer = ItemUpdateSerializer(item, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            updated_item_serializer = ItemResponseSerializer(item)
            return Response(updated_item_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# アイテムの削除
class ItemDelete(generics.RetrieveUpdateAPIView):

    # DELETEリクエストの処理（退会）
    def delete(self, request):
        user = request.user
        response_user = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "user_icon": user.user_icon
        }
        user.delete()
        return Response(response_user, status=status.HTTP_200_OK)


    
    '''
    このメソッドを追加して、どのHTTPメソッドも受け入れるようにします（デバッグ用）
    def options(self, request, *args, **kwargs):
        response = super(ItemUpdate, self).options(request, *args, **kwargs)
        response['Allow'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        return response

    ''' 