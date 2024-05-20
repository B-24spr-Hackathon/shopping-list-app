from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List, Member
from shop.serializers.apply import OwnListsSerializer

class ApplyViewTestCase(APITestCase):
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

        # 申請者
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

    # 申請者が有効なuser_idを送信 200が期待される
    def test_get_apply_valid_user_id(self):
        print("\n[[ InviteViewTestCase/test_get_apply_valid_user_id ]]")

        user_id = 'owner'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }   
        expected_response_data = OwnListsSerializer([self.list_instance], many=True).data
        expected_response = {
            'user_id': 'owner',
            'user_name': 'owner',
            'user_icon': None,
            'lists': expected_response_data
        }
        response = self.client.get(url, headers=headers, format='json')

        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)


    # 申請者が無効なuser_idを送信 404エラーが期待される 
    def test_get_apply_invalid_user_id(self):
        print("\n[[ InviteViewTestCase/test_get_apply_invalid_user_id ]]")

        user_id = 'invalid_user'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token

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

    # 申請者が有効なlist_id,user_idを送信 200が期待される
    def test_post_apply_valid_list_id_and_user_id(self):
        print("\n[[ InviteViewTestCase/test_post_apply_valid_list_id_and_user_id ]]")

        user_id = 'owner'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        } 
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
            "member_status": 2,
        }
        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # 申請者が無効なlist_idを送信 404エラーが期待される
    def test_post_apply_invalid_list_id(self):
        print("\n[[ InviteViewTestCase/test_post_apply_invalid_list_id ]]")

        user_id = 'owner'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }
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

    # 申請者が無効なuser_idを送信 404エラーが期待される
    def test_post_apply_invalid_user_id(self):
        print("\n[[ InviteViewTestCase/test_post_apply_invalid_user_id ]]")

        user_id = 'owner'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }
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

    # 申請者がすでに参加済みまたは招待・申請中のリストのリストに送信 400エラーが期待される
    def test_post_apply_already_member(self):
        print("\n[[ InviteViewTestCase/test_post_apply_already_member ]]")
        
        member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=User.objects.get(user_id='guest'),
            authority=False,
            member_status=0 or 1 or 2,
        )
        member.save()

        user_id = 'owner'  
        url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }
        data = {
            'list_id': self.list_instance.list_id,
            'user_id': 'guest',  
            'authority': True,
        }       
        expected_response = {"error": "あなたはこのリストにすでに参加済み、または招待・申請中です"}

        response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーが自分のリストに申請送信　400エラーが期待される
    def test_post_apply_owner_self(self):
      print("\n[[ InviteViewTestCase/test_post_apply_owner_self ]]")

      user_id = 'owner'  
      url = f'/api/apply/{user_id}/' # url取得がうまくいかないため直接指定
      token = self.list_owner_token
      headers = {
          "Cookie": f"jwt_token={str(token)}"
      }

      data = {
          'list_id': self.list_instance.list_id,
          'user_id': 'owner', 
          'authority': False,
      }     
      expected_response = {"error": "オーナ自身のリストには申請できません"}

      response = self.client.post(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

      # HTTPステータスコードの確認
      print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      # レスポンスデータの確認
      print('[Result]: ', response.data)
      print('[Expect]: ', expected_response)
      self.assertEqual(response.data, expected_response)
