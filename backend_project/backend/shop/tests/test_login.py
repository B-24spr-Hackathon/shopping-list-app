import jwt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User


# 全テスト同じ項目を定義
url = reverse("login")

"""
LoginViewTestCase
LoginViewクラスPOSTリクエストのテストケース
"""
class LoginViewTestCase(APITestCase):
    # 初期値を設定
    def setUp(self):
        User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test")
        )

    # JWTを検証、データを抽出する関数
    def verify_jwt(self, data):
        try:
            payload = jwt.decode(data, settings.JWT_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            return user_id
        except Exception:
            return False

    # 登録済みのユーザー
    def test_ok_data(self):
        print("\n[[ LoginViewTestCase/test_ok_data(4) ]]")

        data = {"email": "test@sample.com", "password": "test"}

        expected_response = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None
        }

        response = self.client.post(url, data, format="json")

        # レスポンスからJWTを抜出す
        try:
            response_jwt = response.data["access"]
            user_id = self.verify_jwt(response_jwt)
        except:
            user_id = False
            print("[Result]: ", "JWT付与なし")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータ（user部分）の確認
        print("[Result]: ", response.data["user"])
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data["user"], expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", "test")
        self.assertEqual(user_id, "test")

    # 未登録のユーザー
    def test_ng_data(self):
        print("\n[[ LoginViewTestCase/test_ng_data(4) ]]")

        data = {"email": "hoge@sample.com", "password": "hoge"}

        expected_response = {"non_field_errors": ["ユーザーは存在しません"]}

        response = self.client.post(url, data, format="json")

        # レスポンスからJWTを抜出す
        try:
            response_jwt = response.data["access"]
            user_id = self.verify_jwt(response_jwt)
        except:
            user_id = False
            print("[Result]: ", "JWT付与なし")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータ（user部分）の確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # パスワードの異なるユーザー
    def test_ng_password(self):
        print("\n[[ LoginViewTestCase/test_ng_password(4) ]]")

        data = {"email": "test@sample.com", "password": "hoge"}

        expected_response = {"non_field_errors": ["ユーザーは存在しません"]}

        response = self.client.post(url, data, format="json")

        # レスポンスからJWTを抜出す
        try:
            response_jwt = response.data["access"]
            user_id = self.verify_jwt(response_jwt)
        except:
            user_id = False
            print("[Result]: ", "JWT付与なし")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータ（user部分）の確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)
