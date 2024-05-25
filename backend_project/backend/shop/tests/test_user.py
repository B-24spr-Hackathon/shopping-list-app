import jwt
from datetime import time
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List, Member, Item


# 全テスト同じ項目を定義
url = reverse("user")

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
            password=make_password("test")
        )

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
    # 正常なリクエストのテスト（リスト無しのユーザー）
    def test_ok_user_no_lists(self):
        print("\n[[ UserGetViewTestCase/test_ok_user_no_lists(2) ]]")
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test")
        )
        user.save()
        token = AccessToken.for_user(user)

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

        response = self.client.get(url, headers=headers)

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
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            have_list=True,
        )
        user.save()
        token = AccessToken.for_user(user)

        list1 = List.objects.create(
            owner_id=user, list_name="test-list", shopping_day=10
        )
        list1.save()

        list2 = List.objects.create(
            owner_id=user, list_name="test-list2", shopping_day=10
        )
        list2.save()

        headers = {"Cookie": f"jwt_token={str(token)}"}

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
                "have_list": True,
                "default_list": True,
                "remind": False,
                "remind_timing": 0,
                "remind_time": None,
            },
            "lists": [
                {
                    "list_id": list1.list_id,
                    "list_name": "test-list",
                    "is_owner": True,
                    "authority": True,
                },
                {
                    "list_id": list2.list_id,
                    "list_name": "test-list2",
                    "is_owner": True,
                    "authority": True,
                },
            ],
        }

        response = self.client.get(url, headers=headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)

    # 正常なリクエストのテスト（共有リスト有りのユーザー）
    def test_ok_user_have_shared_lists(self):
        print("\n[[ UserGetViewTestCase/test_ok_user_have_shared_lists(2) ]]")
        # テスト対象のユーザー
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            have_list=True,
        )
        user.save()
        token = AccessToken.for_user(user)

        # 共有リストのオーナー
        owner = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password="hoge",
            have_list=True
        )
        owner.save()

        # サンプルユーザーのリスト
        user_list = List.objects.create(owner_id=user, list_name="test-list", shopping_day=10)
        user_list.save()

        # 共有するリスト
        owner_list = List.objects.create(owner_id=owner, list_name="hoge-list", shopping_day=5)
        owner_list.save()

        Member.objects.create(list_id=owner_list, guest_id=user, authority=False, member_status=0)

        headers = {"Cookie": f"jwt_token={str(token)}"}

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
                "have_list": True,
                "default_list": True,
                "remind": False,
                "remind_timing": 0,
                "remind_time": None,
            },
            "lists": [
                {
                    "list_id": user_list.list_id,
                    "list_name": "test-list",
                    "is_owner": True,
                    "authority": True,
                },
                {
                    "list_id": owner_list.list_id,
                    "list_name": "hoge-list",
                    "is_owner": False,
                    "authority": False,
                },
            ],
        }

        response = self.client.get(url, headers=headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)

    # JWTの無いリクエスト
    def test_no_jwt(self):
        print("\n[[ UserGetViewTestCase/test_no_jwt(2) ]]")
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            have_list=True,
        )
        user.save()

        List.objects.create(owner_id=user, list_name="test-list", shopping_day=10)

        headers = {"Cookie": "jwt_token="}

        expected_response = {"detail": "トークンが存在しません"}

        response = self.client.get(url, headers=headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)

    # 不正なJWTリクエスト
    def test_ng_jwt(self):
        print("\n[[ UserGetViewTestCase/test_ng_jwt(2) ]]")
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            have_list=True,
        )
        user.save()
        token = AccessToken.for_user(user)
        ng_token = str(token).replace("a", "b", 1)

        List.objects.create(owner_id=user, list_name="test-list", shopping_day=10)

        headers = {"Cookie": f"jwt_token={ng_token}"}

        expected_response = {"detail": "トークンが無効です"}

        response = self.client.get(url, headers=headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)


"""
UserPatchViewTestCase
UserViewクラスPATCHリクエストのテストケース
"""
class UserPatchViewTestCase(APITestCase):
    # 初期値を設定
    def setUp(self):
        user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test")
        )
        user.save()
        self.token = AccessToken.for_user(user)
        self.headers = {"Cookie": f"jwt_token={str(self.token)}"}

        # DBから取得するユーザーの属性
        self.attr = ["user_id", "user_name", "email", "line_id", "line_status",
                "user_icon", "invitation", "request", "have_list",
                "default_list", "remind", "remind_timing", "remind_time"]

    # user_idの更新リクエスト
    def test_user_id(self):
        print("\n[[ UserPatchViewTestCase/test_user_id(3) ]]")

        data = {"user_id": "hoge"}

        expected_response = {"error": "user_idの更新はできません"}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # user_nameの更新リクエスト
    def test_user_name(self):
        print("\n[[ UserPatchViewTestCase/test_user_name(3) ]]")

        data = {"user_name": "hoge"}

        expected_response = {"user": {"user_name": "hoge"}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "hoge",
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのuser_nameの更新リクエスト
    def test_user_name_ng(self):
        print("\n[[ UserPatchViewTestCase/test_user_name_ng(3) ]]")

        data = {"user_name": True}

        expected_response = {"user_name": ["Not a valid string."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # emailの更新リクエスト
    def test_email(self):
        print("\n[[ UserPatchViewTestCase/test_email(3) ]]")

        data = {"email": "hoge@sample.com"}

        expected_response = {"user": {"email": "hoge@sample.com"}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "hoge@sample.com",
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 不正な値でのemailの更新リクエスト
    def test_email_ng(self):
        print("\n[[ UserPatchViewTestCase/test_email_ng(3) ]]")

        data = {"email": "hogesample.com"}

        expected_response = {"email": ["有効なメールアドレスを入力してください。"]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # passwordの更新リクエスト
    def test_password(self):
        print("\n[[ UserPatchViewTestCase/test_password(3) ]]")

        data = {"password": "hoge"}

        expected_response = {"user": {}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # line_idの更新リクエスト
    def test_line_id(self):
        print("\n[[ UserPatchViewTestCase/test_line_id(3) ]]")

        data = {"line_id": "hoge"}

        expected_response = {"error": "line_idの更新はできません"}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # line_statusの更新リクエスト
    def test_line_status(self):
        print("\n[[ UserPatchViewTestCase/test_line_status(3) ]]")

        data = {"line_status": True}

        expected_response = {"error": "line_statusの更新はできません"}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # user_iconの更新リクエスト
    def test_user_icon(self):
        print("\n[[ UserPatchViewTestCase/test_user_icon(3) ]]")

        data = {"user_icon": "test"}

        expected_response = {"user": {"user_icon": "test"}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": "test",
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのuser_iconの更新リクエスト
    def test_user_icon_ng(self):
        print("\n[[ UserPatchViewTestCase/test_user_icon_ng(3) ]]")

        data = {"user_icon": True}

        expected_response = {"user_icon": ["Not a valid string."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # invitationの更新リクエスト
    def test_invitation(self):
        print("\n[[ UserPatchViewTestCase/test_invitation(3) ]]")

        data = {"invitation": True}

        expected_response = {"user": {"invitation": True}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": None,
            "invitation": True,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのinvitationの更新リクエスト
    def test_invitation_ng(self):
        print("\n[[ UserPatchViewTestCase/test_invitation_ng(3) ]]")

        data = {"invitation": 123}

        expected_response = {"invitation": ["Must be a valid boolean."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # requestの更新リクエスト
    def test_request(self):
        print("\n[[ UserPatchViewTestCase/test_request(3) ]]")

        data = {"request": True}

        expected_response = {"user": {"request": True}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": None,
            "invitation": False,
            "request": True,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのrequestの更新リクエスト
    def test_request_ng(self):
        print("\n[[ UserPatchViewTestCase/test_request_ng(3) ]]")

        data = {"request": 123}

        expected_response = {"request": ["Must be a valid boolean."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # have_listの更新リクエスト
    def test_have_list(self):
        print("\n[[ UserPatchViewTestCase/test_have_list(3) ]]")

        data = {"have_list": True}

        expected_response = {"error": "have_listの更新はできません"}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # default_listの更新リクエスト
    def test_default_list(self):
        print("\n[[ UserPatchViewTestCase/test_default_list(3) ]]")

        data = {"default_list": False}

        expected_response = {"user": {"default_list": False}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": False,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # default_listの更新リクエスト
    def test_default_list_ng(self):
        print("\n[[ UserPatchViewTestCase/test_default_list_ng(3) ]]")

        data = {"default_list": 123}

        expected_response = {"default_list": ["Must be a valid boolean."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remindをTrueへの更新リクエスト（line_status: False）
    def test_remind_true_status_false(self):
        print("\n[[ UserPatchViewTestCase/test_remind_true_status_false(3) ]]")

        data = {"remind": True}

        expected_response = {"error": "友達追加が必要です"}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remindをFalseへの更新リクエスト（line_status: False）
    def test_remind_false_status_false(self):
        print("\n[[ UserPatchViewTestCase/test_remind_false_status_false(3) ]]")

        data = {"remind": False}

        expected_response = {"user": {"remind": False}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remindをTrueへの更新リクエスト（line_status: True）
    def test_remind_true_status_true(self):
        print("\n[[ UserPatchViewTestCase/test_remind_true_status_true(3) ]]")
        # 定義済みのユーザーのline_statusをTrueに変更
        user = User.objects.get()
        user.line_status = True
        user.save()

        data = {"remind": True}

        expected_response = {"user": {"remind": True}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": True,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remindをFalseへの更新リクエスト（line_status: True）
    def test_remind_false_status_true(self):
        print("\n[[ UserPatchViewTestCase/test_remind_false_status_true(3) ]]")
        # 定義済みのユーザーのline_statusをTrueに変更
        user = User.objects.get()
        user.line_status = True
        user.save()

        data = {"remind": False}

        expected_response = {"user": {"remind": False}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのremindの更新リクエスト（line_status: True）
    def test_remind_false_status_true_ng(self):
        print("\n[[ UserPatchViewTestCase/test_remind_false_status_true_ng(3) ]]")
        # 定義済みのユーザーのline_statusをTrueに変更
        user = User.objects.get()
        user.line_status = True
        user.save()

        data = {"remind": 123}

        expected_response = {"remind": ["Must be a valid boolean."]}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": None,
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remind_timingの更新リクエスト
    def test_remind_timing(self):
        print("\n[[ UserPatchViewTestCase/test_remind_timing(3) ]]")

        data = {"remind_timing": 3}

        expected_response = {"user": {"remind_timing": 3}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
            "remind_timing": 3,
            "remind_time": None,
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのremind_timingの更新リクエスト
    def test_remind_timing_ng(self):
        print("\n[[ UserPatchViewTestCase/test_remind_timing_ng(3) ]]")

        data = {"remind_timing": True}

        expected_response = {"remind_timing": ['"True"は有効な選択肢ではありません。']}

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # remind_timeの更新リクエスト
    def test_remind_time(self):
        print("\n[[ UserPatchViewTestCase/test_remind_time(3) ]]")

        data = {"remind_time": "09:00"}

        expected_response = {"user": {"remind_time": "09:00:00"}}

        response = self.client.patch(url, data=data, headers=self.headers, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
            "remind_time": time(9, 0),
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 違う型でのremind_timeの更新リクエスト
    def test_remind_time_ng(self):
        print("\n[[ UserPatchViewTestCase/test_remind_time_ng(3) ]]")

        data = {"remind_time": 9}

        expected_response = {
            "remind_time": [
                "時刻の形式が違います。以下のどれかの形式にしてください: hh:mm[:ss[.uuuuuu]]。"
            ]
        }

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # データの一括更新リクエスト
    def test_all(self):
        print("\n[[ UserPatchViewTestCase/test_all(3) ]]")

        data = {
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "user_icon": "hoge",
            "invitation": True,
            "request": True,
            "default_list": False,
            "remind_timing": 3,
            "remind_time": "9:00"
        }

        expected_response = {
            "user": {
                "user_name": "hoge",
                "email": "hoge@sample.com",
                "user_icon": "hoge",
                "invitation": True,
                "request": True,
                "default_list": False,
                "remind_timing": 3,
                "remind_time": "09:00:00",
            }
        }

        response = self.client.patch(
            url, data=data, headers=self.headers, format="json"
        )

        user = list(User.objects.values(*self.attr))
        db_user = {
            "user_id": "test",
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "line_id": None,
            "line_status": False,
            "user_icon": "hoge",
            "invitation": True,
            "request": True,
            "have_list": False,
            "default_list": False,
            "remind": False,
            "remind_timing": 3,
            "remind_time": time(9, 0),
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # JWTの無い更新リクエスト
    def test_no_jwt(self):
        print("\n[[ UserPatchViewTestCase/test_no_jwt(3) ]]")

        data = {
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "user_icon": "hoge",
            "invitation": True,
            "request": True,
            "default_list": False,
            "remind_timing": 3,
            "remind_time": "9:00",
        }

        expected_response = {"detail": "トークンが存在しません"}

        response = self.client.patch(url, data=data, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)

    # 不正なJWTでの更新リクエスト
    def test_ng_jwt(self):
        print("\n[[ UserPatchViewTestCase/test_ng_jwt(3) ]]")

        # トークンを改ざん
        token = str(self.token).replace("a", "b")
        headers = {"Cookie": f"jwt_token={token}"}

        data = {
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "user_icon": "hoge",
            "invitation": True,
            "request": True,
            "default_list": False,
            "remind_timing": 3,
            "remind_time": "9:00",
        }

        expected_response = {"detail": "トークンが無効です"}

        response = self.client.patch(url, headers=headers ,data=data, format="json")

        user = list(User.objects.values(*self.attr))
        db_user = {
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
        }

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", db_user)
        self.assertEqual(user[0], db_user)


"""
UserDeleteViewTestCase
UserViewクラスDELETEリクエストのテストケース
"""
class UserDeleteViewTestCase(APITestCase):
    # 初期値を設定
    def setUp(self):
        self.user = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test")
        )
        self.user.save()
        self.token = AccessToken.for_user(self.user)
        self.headers = {"Cookie": f"jwt_token={str(self.token)}"}

        self.expected_response = {
            "user_id": self.user.user_id,
            "user_name": self.user.user_name,
            "email": self.user.email,
            "user_icon": self.user.user_icon,
        }

    # 登録済みユーザー（リスト無し）の削除リクエスト
    def test_delete_exist_user(self):
        print("\n[[ UserDeleteViewTestCase/test_delete_exist_user(3) ]]")

        response = self.client.delete(url, headers=self.headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", self.expected_response)
        self.assertEqual(response.data, self.expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)

    # 登録済みユーザー（リスト有り）の削除リクエスト
    def test_delete_exist_user_have_list(self):
        print("\n[[ UserDeleteViewTestCase/test_delete_exist_user_have_list(4) ]]")

        self.user.have_list = True
        self.user.save()

        # リストの作成
        List.objects.create(owner_id=self.user, list_name="test-list", shopping_day=10)

        response = self.client.delete(url, headers=self.headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", self.expected_response)
        self.assertEqual(response.data, self.expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # listsテーブルのレコード数の確認
        print("[Result]: ", "lists", List.objects.count(), "==", 0)
        self.assertEqual(List.objects.count(), 0)

    # 登録済みユーザー（リスト・アイテム有り）の削除リクエスト
    def test_delete_exist_user_have_list_and_item(self):
        print("\n[[ UserDeleteViewTestCase/test_delete_exist_user_have_list_and_item(5) ]]")

        self.user.have_list = True
        self.user.save()

        # リストの作成
        list = List.objects.create(owner_id=self.user, list_name="test-list", shopping_day=10)
        list.save()

        # アイテムの作成
        Item.objects.create(item_name="洗剤", list_id=list)

        response = self.client.delete(url, headers=self.headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", self.expected_response)
        self.assertEqual(response.data, self.expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 0)
        self.assertEqual(User.objects.count(), 0)
        # listsテーブルのレコード数の確認
        print("[Result]: ", "lists", List.objects.count(), "==", 0)
        self.assertEqual(List.objects.count(), 0)
        # itemsテーブルのレコード数の確認
        print("[Result]: ", "items", Item.objects.count(), "==", 0)
        self.assertEqual(Item.objects.count(), 0)

    # 登録済みユーザー（リスト・アイテム・共有（オーナー）有り）の削除リクエスト
    def test_delete_exist_user_have_list_and_item_and_own_member(self):
        print(
            "\n[[ UserDeleteViewTestCase/test_delete_exist_user_have_list_and_item_and_own_member(6) ]]"
        )

        self.user.have_list = True
        self.user.save()

        # 共有ユーザーの作成
        member = User.objects.create(user_id="hoge", user_name="hoge", email="hoge@sample.com", password="hoge")
        member.save()

        # リストの作成
        list = List.objects.create(
            owner_id=self.user, list_name="test-list", shopping_day=10
        )
        list.save()

        # アイテムの作成
        Item.objects.create(item_name="洗剤", list_id=list)

        # 共有の追加
        Member.objects.create(list_id=list, guest_id=member, authority=False, member_status=0)

        response = self.client.delete(url, headers=self.headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", self.expected_response)
        self.assertEqual(response.data, self.expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)
        # listsテーブルのレコード数の確認
        print("[Result]: ", "lists", List.objects.count(), "==", 0)
        self.assertEqual(List.objects.count(), 0)
        # itemsテーブルのレコード数の確認
        print("[Result]: ", "items", Item.objects.count(), "==", 0)
        self.assertEqual(Item.objects.count(), 0)
        # membersテーブルのレコード数の確認
        print("[Result]: ", "members", Member.objects.count(), "==", 0)
        self.assertEqual(Member.objects.count(), 0)

    # 登録済みユーザー（リスト・アイテム・共有（メンバー）有り）の削除リクエスト
    def test_delete_exist_user_have_list_and_item_and_member(self):
        print(
            "\n[[ UserDeleteViewTestCase/test_delete_exist_user_have_list_and_item_and_member(6) ]]"
        )

        self.user.have_list = True
        self.user.save()

        # オーナーユーザーの作成
        owner = User.objects.create(
            user_id="hoge", user_name="hoge", email="hoge@sample.com", password="hoge"
        )
        owner.save()

        # 共有リストの作成
        shared_list = List.objects.create(owner_id=owner, list_name="hoge-list", shopping_day=5)

        # リストの作成
        list = List.objects.create(
            owner_id=self.user, list_name="test-list", shopping_day=10
        )
        list.save()

        # アイテムの作成
        Item.objects.create(item_name="洗剤", list_id=list)

        # 共有の追加
        Member.objects.create(
            list_id=shared_list, guest_id=self.user, authority=False, member_status=0
        )

        response = self.client.delete(url, headers=self.headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", self.expected_response)
        self.assertEqual(response.data, self.expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)
        # listsテーブルのレコード数の確認
        print("[Result]: ", "lists", List.objects.count(), "==", 1)
        self.assertEqual(List.objects.count(), 1)
        # itemsテーブルのレコード数の確認
        print("[Result]: ", "items", Item.objects.count(), "==", 0)
        self.assertEqual(Item.objects.count(), 0)
        # membersテーブルのレコード数の確認
        print("[Result]: ", "members", Member.objects.count(), "==", 0)
        self.assertEqual(Member.objects.count(), 0)

    # JWTの無いリクエスト
    def test_no_jwt(self):
        print("\n[[ UserDeleteViewTestCase/test_no_jwt(3) ]]")

        expected_response = {"detail": "トークンが存在しません"}

        response = self.client.delete(url)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)

    # 不正なJWTのリクエスト
    def test_ng_jwt(self):
        print("\n[[ UserDeleteViewTestCase/test_ng_jwt(3) ]]")

        # トークンを改ざん
        token = str(self.token).replace("a", "b")
        headers = {"Cookie": f"jwt_token={token}"}

        expected_response = {"detail": "トークンが無効です"}

        response = self.client.delete(url, headers=headers)

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print("[Result]: ", response.data)
        print("[Expect]: ", expected_response)
        self.assertEqual(response.data, expected_response)
        # usersテーブルのレコード数の確認
        print("[Result]: ", "users", User.objects.count(), "==", 1)
        self.assertEqual(User.objects.count(), 1)