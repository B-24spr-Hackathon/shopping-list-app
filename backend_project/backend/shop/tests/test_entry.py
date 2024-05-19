from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List, Member

class EntryViewTestCase(APITestCase):
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

        # リストインスタンス
        list_instance = List.objects.create(
            owner_id=list_owner,
            list_name='test-list',
        )
        list_instance.save()
        self.list_instance = list_instance

        # ゲスト
        guest_member = User.objects.create(
            user_id='guest',
            user_name='guest',
            email='guest@sample,com',
            password='guest'
        )
        guest_member.save()
        self.guest_member_token = AccessToken.for_user(guest_member)

        # Member作成
        member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=guest_member,
            member_status=0,
            authority=False,
        )
        self.member_id = member.pk         
        
    # PATCHメソッドのテスト
    
    # オーナーが有効なmember_idに送信 200が期待される
    def test_patch_entry_valid_user_id_as_owner(self):
        print("\n[[ EntryViewTestCase/test_patch_entry_valid_user_id_as_owner ]]")

        member_ids = Member.objects.filter(list_id=self.list_instance, member_status__in=[0, 1, 2]).values_list('pk', flat=True)

        member_id = member_ids[0]

        url = f'/api/entry/{member_id}/' # url取得がうまくいかないため直接指定      
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        } 
        data = {
            'authority': True,
        }
        expected_response = {
            'authority': True,
        }
        response = self.client.patch(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

         # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)


    # ゲストが有効なmember_idに送信 403エラーが期待される
    def test_patch_entry_valid_user_id_as_guest(self):
        print("\n[[ EntryViewTestCase/test_patch_entry_valid_user_id_as_guest ]]")

        member_ids = Member.objects.filter(list_id=self.list_instance, member_status__in=[0, 1, 2]).values_list('pk', flat=True)

        member_id = member_ids[0]

        url = f'/api/entry/{member_id}/' # url取得がうまくいかないため直接指定      
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        } 
        data = {
            'authority': True,
        }
        expected_response = {
            'authority': True,
        }
        response = self.client.patch(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

         # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', {"detail": "アクセスする権限がありません"})
        self.assertEqual(response.data, {"detail": "アクセスする権限がありません"})


    # DELETEメソッドのテスト

    # オーナーがmember_status=0の有効なmember_idに送信　200が期待される
    def test_delete_entry_valid_user_id(self):
        print("\n[[ EntryViewTestCase/test_delete_entry_valid_user_id ]]")

        member_ids = Member.objects.filter(list_id=self.list_instance, member_status=0).values_list('pk', flat=True)

        member_id = member_ids[0]
        url = f'/api/entry/{member_id}/' # url取得がうまくいかないため直接指定      
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }         
        expected_response = {
            'user_name': 'guest'
        }
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)   
      
       
    # オーナーが無効なmember_idに送信、404エラーが期待される
    def test_delete_entry_invalid_user_id(self):
        print("\n[[ EntryViewTestCase/test_delete_entry_invalid_user_id ]]")

        # 存在しないmember_idを使用
        invalid_member_id = 9999

        url = f'/api/entry/{invalid_member_id}/'  # url取得がうまくいかないため直接指定      
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }         
        expected_response = {'error': 'メンバーが存在しません'}
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーがmember_status=1の有効なmember_idに送信　エラーが期待される 
    def test_delete_entry_with_member_status_is_1(self):
        print("\n[[ EntryViewTestCase/test_delete_entry_with_member_status_is_1 ]]")

        # すでに存在する 'guest' ユーザーを取得
        guest_member = User.objects.get(user_id='guest')

        new_member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=guest_member,
            member_status=1,  # member_status を 1 に設定
            authority=False,
        )        
        member_id = new_member.pk

        url = f'/api/entry/{member_id}/'
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }
        data = {}
        expected_response = {
            'error': '招待・申請中のゲストの削除はここからはできません',
        }
        response = self.client.delete(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)
        
        # オーナーがmember_status=2の有効なmember_idに送信　エラーが期待される 'error': '招待・申請中のゲストの削除はここからはできません' 
    def test_delete_entry_with_member_status_is_2(self):
        print("\n[[ EntryViewTestCase/test_delete_entry_with_member_status_is_2 ]]")

        # すでに存在する 'guest' ユーザーを取得
        guest_member = User.objects.get(user_id='guest')

        new_member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=guest_member,
            member_status=2,  # member_status を 1 に設定
            authority=False,
        )        
        member_id = new_member.pk

        url = f'/api/entry/{member_id}/'
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }
        data = {}
        expected_response = {
            'error': '招待・申請中のゲストの削除はここからはできません',
        }
        response = self.client.delete(url, data, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)


# ゲストが有効なmember_idに送信　403エラーが期待される
    def test_delete_entry_as_guest(self):
        print("\n[[ EntryViewTestCase/test_delete_entry_as_guest ]]")

        member_ids = Member.objects.filter(list_id=self.list_instance, member_status=0).values_list('pk', flat=True)

        member_id = member_ids[0]
        url = f'/api/entry/{member_id}/' # url取得がうまくいかないため直接指定      
        token = self.guest_member_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }         
        expected_response = {
            "detail":"アクセスする権限がありません"
        }
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response) 
