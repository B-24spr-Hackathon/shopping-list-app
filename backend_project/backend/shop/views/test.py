from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import requests


class TestView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        url = settings.PUSH_URL
        token = settings.CHANNEL_ACCESS_TOKEN
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "to": "U00db4ac5f595404949226fd28282f6d0",
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "buttons",
                        "text": "洗剤がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "追加する",
                                "data": "to_list=true",
                            },
                            {
                                "type": "message",
                                "label": "追加しない",
                                "text": "Not yet",
                            },
                        ],
                    },
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        return Response(response.text, status=status.HTTP_200_OK)
