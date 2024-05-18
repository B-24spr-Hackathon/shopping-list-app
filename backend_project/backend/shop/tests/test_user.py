import jwt
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List


"""
UserPostViewTestCase
UserViewクラスPOSTリクエストのテストケース
"""
class UserPostViewTestCase(APITestCase):
    # JWT検証用の関数
    def verify_jwt(self, data):
        try:
            payload = jwt.decode(data, settings.JWT_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            return user_id
        except Exception:
            return False

    # 正常なリクエストのテスト
    def test_ok_data(self):
        print("\n[[ UserPostViewTestCase/test_ok_data(4) ]]")
        url = reverse("user")
        data = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "password": "test",
        }

        expected_response = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
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
        print("[Result]: ", response.status_code, "==", status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)
        # レスポンスデータ（user部分）の確認
        print("[Result]: ", response.data["user"])
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data["user"], expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", "test")
        self.assertEqual(user_id, "test")

    # emailの形式が不正なリクエストのテスト
    def test_bad_email(self):
        print("\n[[ UserPostViewTestCase/test_bad_email(5) ]]")

        url = reverse("user")
        data = {
            "user_id": "test",
            "user_name": "test",
            "email": "testsample.com",
            "password": "test",
        }

        expected_response = {"email": ["有効なメールアドレスを入力してください。"]}

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
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # ボディのないリクエストのテスト
    def test_no_body(self):
        print("\n[[ UserPostViewTestCase/test_no_body(5) ]]")

        url = reverse("user")

        expected_response = {
            "user_id": ["この項目は必須です。"],
            "user_name": ["この項目は必須です。"],
            "email": ["この項目は必須です。"],
            "password": ["この項目は必須です。"],
        }

        response = self.client.post(url, format="json")

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
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 全項目空文字のリクエストのテスト
    def test_all_empty(self):
        print("\n[[ UserPostViewTestCase/test_all_empty(5) ]]")

        url = reverse("user")
        data = {
            "user_id": "",
            "user_name": "",
            "email": "",
            "password": "",
        }

        expected_response = {
            "user_id": ["この項目は空にできません。"],
            "user_name": ["この項目は空にできません。"],
            "email": ["この項目は空にできません。"],
            "password": ["この項目は空にできません。"]
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
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 全項目Noneのリクエストのテスト
    def test_all_none(self):
        print("\n[[ UserPostViewTestCase/test_all_none(5) ]]")

        url = reverse("user")
        data = {
            "user_id": None,
            "user_name": None,
            "email": None,
            "password": None,
        }

        expected_response = {
            "user_id": ["この項目はnullにできません。"],
            "user_name": ["この項目はnullにできません。"],
            "email": ["この項目はnullにできません。"],
            "password": ["この項目はnullにできません。"],
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
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 登録済みのリクエストのテスト
    def test_exist_user_id(self):
        print("\n[[ UserPostViewTestCase/test_exist_user_id(5) ]]")

        User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password="test"
        )

        url = reverse("user")
        data = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "password": "test",
        }

        expected_response = {
            "user_id": ["登録済みのIDです"],
            "email": ["登録済みのメールアドレスです"]
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
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 型の異なるuser_idのテスト
    def test_invalid_user_id(self):
        print("\n[[ UserPostViewTestCase/test_invalid_user_id(5) ]]")

        url = reverse("user")
        data = {
            "user_id": True,
            "user_name": "test",
            "email": "test@sample.com",
            "password": "test",
        }

        expected_response = {"user_id": ["Not a valid string."]}

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
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 型の異なるuser_nameのテスト
    def test_invalid_user_name(self):
        print("\n[[ UserPostViewTestCase/test_invalid_user_name(5) ]]")

        url = reverse("user")
        data = {
            "user_id": "test",
            "user_name": True,
            "email": "test@sample.com",
            "password": "test",
        }

        expected_response = {"user_name": ["Not a valid string."]}

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
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)

    # 型の異なるpasswordのテスト
    def test_invalid_password(self):
        print("\n[[ UserPostViewTestCase/test_invalid_password(5) ]]")

        url = reverse("user")
        data = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "password": True,
        }

        expected_response = {"password": ["Not a valid string."]}

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
        # 登録されたレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # JWTの確認
        print("[Result]: ", user_id, "==", False)
        self.assertEqual(user_id, False)


"""
UserGetViewTestCase
UserViewクラスGETリクエストのテストケース
"""
class UserGetViewTestCase(APITestCase):
    # テスト用データのセットアップ
    def setUp(self):

        # リストを持つユーザー
        user_have_lists = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password="hoge",
            have_list=True
        )
        user_have_lists.save()
        self.user_have_lists_token = AccessToken.for_user(user_have_lists)

        list = List.objects.create(
            owner_id=user_have_lists,
            list_name="hoge-list",
            shopping_day=10
        )
        list.save()

    # 正常なリクエストのテスト（リスト無しのユーザー）
    def test_ok_user_no_lists(self):
        print("\n[[ UserGetViewTestCase/test_ok_user_no_lists(2) ]]")
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password="test"
        )
        user.save()
        token = AccessToken.for_user(user)
        url = reverse("user")
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }

        expected_response = {
            "user": {
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
                "remind_time": None,
            },
            "lists": []
        }

        response = self.client.get(url, headers=headers, format="json")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)

    # 正常なリクエストのテスト（リスト有りのユーザー）
    def test_ok_user_have_lists(self):
        print("\n[[ UserGetViewTestCase/test_ok_user_have_lists(2) ]]")
        user = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password="hoge",
            have_list=True,
        )
        user.save()
        token = AccessToken.for_user(user)

        List.objects.create(
            owner_id=user,
            list_name="hoge-list",
            shopping_day=10
        )
        url = reverse("user")
        headers = {"Cookie": f"jwt_token={str(token)}"}

        expected_response = {
            "user": {
                "user_id": "hoge",
                "user_name": "hoge",
                "email": "hoge@sample.com",
                "line_id": None,
                "line_status": False,
                "user_icon": None,
                "invitation": False,
                "request": False,
                "have_list": True,
                "default_list": True,
                "remind": False,
                "remind_timing": 0,
                "remind_time": None,
            },
            "lists": [
                {
                    "list_id": 1,
                    "list_name": "hoge-list",
                    "is_owner": True,
                    "authority": True,
                }
            ],
        }

        response = self.client.get(url, headers=headers, format="json")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
