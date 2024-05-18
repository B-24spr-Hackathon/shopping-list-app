from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List, Member


class InviteViewTestCase(APITestCase):
    # テスト用データのセットアップ
    def setUp(self):
        
        # リストオーナー
        list_owner = User.objects.create(
            user_id='owner',
            user_name='owner',
            email='owner@sample,com',
            password='owner'
        )
        list_owner.save()
        self.list_owner_token = AccessToken.for_user(list_owner)

        # 招待者
        guest_member = User.objects.create(
            user_id='guest',
            user_name='guest',
            email='guest@sample,com',
            password='guest'
        )
        guest_member.save()
        self.guest_member_token = AccessToken.for_user(guest_member)

        list_instance = List.objects.create(
            owner_id=list_owner,
            list_name='test-list',
        )
        list_instance.save()
        self.list_instance = list_instance


  # GETメソッドのテスト

    # listオーナーが有効なuser_idを送信 200が期待される
    def test_get_invite_valid_user_id(self):
        print("\n[[ InviteViewTestCase/test_get_invite_valid_user_id ]]")
        
        token = self.list_owner_token
        url = reverse('find-invitee-get', kwargs={'user_id': 'guest'})
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }        
        expected_response = {
            'user_id':'guest',
            'user_name':'guest',
            'user_icon': None,
        }
        response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # リストオーナーが無効なuser_idを送信 404エラーが期待される 
    def test_get_invite_invalid_user_id(self):
        print("\n[[ InviteViewTestCase/test_get_invite_invalid_user_id ]]")
        
        token = self.list_owner_token
        url = reverse('find-invitee-get', kwargs={'user_id': 'invalid_user'})      

        headers = {
          "Cookie": f"jwt_token={str(token)}"
        }
        response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', {"error": "ユーザーが存在しません"})
        self.assertEqual(response.data, {"error": "ユーザーが存在しません"})


  #POSTメソッドのテスト

    # リストオーナーが有効なlist_id,user_idを送信 200が期待される

    def test_post_invite_valid_list_id_and_user_id(self):
        print("\n[[ InviteViewTestCase/test_post_invite_valid_list_id_and_user_id ]]")

        token = self.list_owner_token
        url = reverse('invitee-post')

        data = {
            'list_id': self.list_instance.list_id,
            'user_id': 'guest',
            'authority': True,
        }
        expected_response = {
            "list_id": self.list_instance.list_id,
            "list_name": "test-list",
            "guest_id": "guest",
            "user_name": "guest",
            "user_icon": None,
            "authority": True,
            "member_status": 1,
        }
        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # リストオーナーが無効なlist_idを送信 404エラーが期待される 
    def test_post_invite_invalid_list_id(self):
        print("\n[[ InviteViewTestCase/test_post_invite_invalid_list_id ]]")

        token = self.list_owner_token
        url = reverse('invitee-post')

        data = {
            'list_id': 999,
            'user_id': 'guest',
            'authority': True,
        }
        expected_response = {'error': 'リストが存在しません'}
        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    #リストオーナーが無効なuser_idを送信 404エラーが期待される
    def test_post_invite_invalid_user_id(self):
        print("\n[[ InviteViewTestCase/test_post_invite_invalid_user_id ]]")

        token = self.list_owner_token
        url = reverse('invitee-post')

        data = {
            'list_id': self.list_instance.list_id,
            'user_id': 'invalid_user',
            'authority': True,
        }
        expected_response = {'error': 'ユーザーが存在しません'}
        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    #リストオーナーがすでに参加済みまたは招待・申請中のゲストに送信 400エラーが期待される
    def test_post_invite_already_member(self):
        print("\n[[ InviteViewTestCase/test_post_invite_already_member ]]")
        
        member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=User.objects.get(user_id='guest'),
            authority=False,
            member_status=0 or 1 or 2,
        )
        member.save()

        token = self.list_owner_token
        url = reverse('invitee-post')

        data = {
            'list_id': self.list_instance.list_id,
            'user_id': 'guest',  
            'authority': True,
        }       
        expected_response = {"error": "このゲストはこのリストにすでに参加済み、または招待・申請中です"}

        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    #リストオーナーが自分宛てに招待を送信 400エラーが期待される オーナー自身を招待できません
    def test_post_invite_owner_self(self):
        print("\n[[ InviteViewTestCase/test_post_invite_owner_self ]]")

        token = self.list_owner_token
        url = reverse('invitee-post')

        data = {
            'list_id': self.list_instance.list_id,
            'user_id': 'owner', 
            'authority': False,
        }     
        expected_response = {"error": "オーナー自身を招待できません"}

        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

        