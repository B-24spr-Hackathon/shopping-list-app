from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from ..models import List
from shop.authentication import CustomJWTAuthentication
from shop.serializers.lists import ListSerializer 

# 買い物リスト表示(GET)
class ListView(APIView):
    serializer_class = ListSerializer
    # 使用するserializerが、リクエストの中からojtを取得する必要があるため
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    def get(self, request, *args, **kwargs):
       # requestから、ログインしているユーザーのuser_idを取得
        user_id = request.user.id
        # owner または invitee, でリストをフィルタリング
        filters = (Q(owner_id=user_id) | Q(list_id__members__invitee_id=user_id)) 
        lists = List.objects.filter(filters)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)    

'''
注意点としては、この方法でauthorityを取得するには、ListSerializerを使用するビューでcontextにrequestオブジェクトを含める必要があります。たとえばAPIViewのget_serializer_contextメソッドをオーバーライドして、requestオブジェクトを含めることができます。

from rest_framework.views import APIView

class ListView(APIView):
    serializer_class = ListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
このようにcontextを設定することで、ListSerializer内のget_authorityメソッドでrequestオブジェクトを利用し、現在のユーザーに関連する情報を取得することができます。
'''