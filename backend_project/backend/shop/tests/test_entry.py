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

        
# 招待 申請承認機能
class EntryAcceptViewTestCase(APITestCase):
    def setUp(self):
        # リストオーナー
        self.list_owner = User.objects.create(
            user_id='owner',
            user_name='owner',
            email='owner@sample.com',
            password='owner'
        )
        self.list_owner_token = AccessToken.for_user(self.list_owner)

        # リストインスタンス
        self.list_instance = List.objects.create(
            owner_id=self.list_owner,
            list_name='test-list',
        )

        # ゲスト
        self.guest_member = User.objects.create(
            user_id='guest',
            user_name='guest',
            email='guest@sample.com',
            password='guest'
        )
        self.guest_member_token = AccessToken.for_user(self.guest_member)

        # 他のユーザー
        self.other_user = User.objects.create(
            user_id='other',
            user_name='other',
            email='other@sample.com',
            password='other'
        )
        self.other_user_token = AccessToken.for_user(self.other_user)

        # member_status=2 のメンバー作成
        self.member_status_2 = Member.objects.create(
            list_id=self.list_instance,
            guest_id=self.guest_member,
            member_status=2,
            authority=False,
        )

        # member_status=1 のメンバー作成
        self.member_status_1 = Member.objects.create(
            list_id=self.list_instance,
            guest_id=self.guest_member,
            member_status=1,
            authority=False,
        )

        # member_status=0 のメンバー作成
        self.member_status_0 = Member.objects.create(
            list_id=self.list_instance,
            guest_id=self.guest_member,
            member_status=0,
            authority=False,
        )

    # オーナーが有効な member_status=2 のメンバー承認。200を期待
    def test_owner_accept_valid_member_status_2(self):
        print("\n[[ EntryAcceptViewTestCase/test_owner_accept_valid_member_status_2 ]]")

        url = f'/api/entry/accept/{self.member_status_2.pk}/'
        token = self.list_owner_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'member_status': 0
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストが自分に来ている招待を正しく承認。 200を期待
    def test_guest_accept_valid_member_status_1_self(self):
        print("\n[[ EntryAcceptViewTestCase/test_guest_accept_valid_member_status_1_self ]]")

        url = f'/api/entry/accept/{self.member_status_1.pk}/'
        token = self.guest_member_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'member_status': 0
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # 存在しないmember_idに対する承認。404を期待
    def test_accept_nonexistent_member(self):
        print("\n[[ EntryAcceptViewTestCase/test_accept_nonexistent_member ]]")

        url = f'/api/entry/accept/9999/'
        token = self.list_owner_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'error': 'ゲストが存在しません'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーでもゲストでもないユーザが承認。403を期待
    def test_accept_without_permission(self):
        print("\n[[ EntryAcceptViewTestCase/test_accept_without_permission ]]")

        url = f'/api/entry/accept/{self.member_status_2.pk}/'
        token = self.other_user_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'error': '承認する権限がありません'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーが自分が所有していないリストの申請を承認。403を期待
    def test_owner_accept_request_from_other_list(self):
        print("\n[[ EntryAcceptViewTestCase/test_owner_accept_request_from_other_list ]]")

        # 他のリストのオーナー
        other_list_owner = User.objects.create(
            user_id='other_owner',
            user_name='other_owner',
            email='other_owner@sample.com',
            password='other_owner'
        )
        # 他のリストインスタンス
        other_list_instance = List.objects.create(
            owner_id=other_list_owner,
            list_name='other-test-list',
        )
        # 他のリストの member_status=2 のメンバー作成
        other_member_status_2 = Member.objects.create(
            list_id=other_list_instance,
            guest_id=self.guest_member,
            member_status=2,
            authority=False,
        )
        url = f'/api/entry/accept/{other_member_status_2.pk}/'
        token = self.list_owner_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'error': '承認する権限がありません'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーがmember_status=1を承認。400を期待
    def test_owner_accept_invalid_member_status(self):
        print("\n[[ EntryAcceptViewTestCase/test_owner_accept_invalid_member_status ]]")

        url = f'/api/entry/accept/{self.member_status_1.pk}/'
        token = self.list_owner_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'error': '自身が招待したものは自身で承認できません'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)       
        
    # ゲストがmember_status=1 の他メンバーを承認。403を期待
    def test_guest_accept_valid_member_status_1(self):
        print("\n[[ EntryAcceptViewTestCase/test_guest_accept_valid_member_status_1 ]]")

        other_member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=self.other_user,
            member_status=1,
            authority=False,
        )
        url = f'/api/entry/accept/{other_member.pk}/'
        token = self.guest_member_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")
        
        expected_response = {
            'error': '承認する権限がありません'
            }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)  

    # ゲストが自分の申請を承認。403を期待
    def test_guest_accept_invalid_member_status(self):
        print("\n[[ EntryAcceptViewTestCase/test_guest_accept_invalid_member_status ]]")

        url = f'/api/entry/accept/{self.member_status_2.pk}/'
        token = self.guest_member_token
        response = self.client.patch(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {
            'error': '自身が申請したものは自身で承認できません'
            }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response) 

# 招待 申請 拒否・中止機能　DELETE
class EntryDeclineViewTestCase(APITestCase):
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

        # 別のユーザー（ゲストでもオーナーでもない）
        another_user = User.objects.create(
            user_id='another',
            user_name='another',
            email='another@sample.com',
            password='another'
        )
        another_user.save()
        self.another_user_token = AccessToken.for_user(another_user)

        # Member作成
        member = Member.objects.create(
            list_id=self.list_instance,
            guest_id=guest_member,
            member_status=1,
            authority=False,
        )
        self.member = member
        self.member_id = member.pk  

    # オーナーが招待を中止 200が期待される
    def test_owner_cancel_invite(self):
        print("\n[[ EntryDeclineViewTestCase/test_owner_cancel_invite ]]")

        url = f'/api/entry/decline/{self.member_id}/'
        token = self.list_owner_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'user_name': 'guest'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # オーナーが申請を拒否 200が期待される
    def test_owner_decline_request(self):
        print("\n[[ EntryDeclineViewTestCase/test_owner_decline_request ]]")

        # member_statusを2に変更
        self.member.member_status = 2
        self.member.save()
        
        url = f'/api/entry/decline/{self.member_id}/'
        token = self.list_owner_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'user_name': 'guest'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストが招待を拒否200が期待される
    def test_guest_decline_invite(self):
        print("\n[[ EntryDeclineViewTestCase/test_guest_decline_invite ]]")

        # member_statusを1に変更
        self.member.member_status = 1
        self.member.save()
        
        url = f'/api/entry/decline/{self.member_id}/'
        token = self.guest_member_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'user_name': 'guest'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

# ゲストが申請を中止 200が期待される
    def test_guest_cancel_request(self):
        print("\n[[ EntryDeclineViewTestCase/test_guest_decline_invite ]]")

        # member_statusを2に変更
        self.member.member_status = 2
        self.member.save()
        
        url = f'/api/entry/decline/{self.member_id}/'
        token = self.guest_member_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'user_name': 'guest'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストが存在しない 404エラーが期待される
    def test_guest_not_found(self):
        print("\n[[ EntryDeclineViewTestCase/test_guest_not_found ]]")

        non_exist_member_id = 99999

        url = f'/api/entry/decline/{non_exist_member_id}/'
        token = self.list_owner_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {"error": "ゲストが存在しません"
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストでもユーザーでもないものがアクセス403{'error': '拒否または中止する権限がありません'}
    def test_nonguest_or_nonowner_access_denied(self):
        print("\n[[ EntryDeclineViewTestCase/test_nonguest_or_nonowner_access_denied ]]")

        url = f'/api/entry/decline/{self.member_id}/'
        token = self.another_user_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'error': '拒否または中止する権限がありません'}
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストが参加済み 400エラーが期待される
    def test_guest_already_participated(self):
        print("\n[[ EntryDeclineViewTestCase/test_guest_already_participated ]]")

        # member_statusを0に変更
        self.member.member_status = 0
        self.member.save()
        
        url = f'/api/entry/decline/{self.member_id}/'
        token = self.list_owner_token
        response = self.client.delete(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")

        expected_response = {'error': '参加済みのゲストの削除はここからはできません'
        }
        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

# 招待・申請一覧を表示 GET
class EntryMemberStatusViewTestCase(APITestCase):
    
    def setUp(self):
        
        # リストオーナー
        list_owner = User.objects.create(
        user_id='owner',
        user_name='owner',
        email='owner@sample,com',
        password='owner'
        )
        list_owner.save()
        self.list_owner = list_owner        
        self.list_owner_token = AccessToken.for_user(list_owner)
        
        guest_member = User.objects.create_user(
            user_id='guest', 
            user_name='guest', 
            email='guest@example.com', 
            password='password'
            )
        guest_member.save()
        self.guest_member = guest_member
        self.guest_user_token = AccessToken.for_user(guest_member)
        
        another_user = User.objects.create_user(
            user_id='another', 
            user_name='another', 
            email='another@example.com', 
            password='password'
            )
        another_user.save()
        self.another_user = another_user
        self.another_user_token = AccessToken.for_user(another_user)

        # リストを作成
        list_instance = List.objects.create(
            owner_id=list_owner, 
            list_name='test-list'
            )
        list_instance.save()
        self.list_instance = list_instance

        # メンバーを作成
        member = Member.objects.create(
            list_id=list_instance, 
            guest_id=guest_member, 
            member_status=1
            )
        member.save()
        self.member = member

    # オーナーとしてリクエスト 200が期待される
    def test_get_entry_status_as_owner(self):
        print("\n[[ EntryMemberStatusViewTestCase/test_get_entry_status_as_owner ]]")

        url = '/api/member_status/'
        token = self.list_owner_token
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }    
        expected_response = [{            
            'member_id': self.member.member_id,
            'guest_name': self.guest_member.user_name,
            'member_status': self.member.member_status,
            'list_id': self.list_instance.list_id,
            'list_name': self.list_instance.list_name,
            'owner_name': self.list_owner.user_name,
            'is_owner': True,
        }]

        response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストとしてリクエスト 200が期待される
    def test_get_entry_status_as_guest(self):
        print("\n[[ EntryMemberStatusViewTestCase/test_get_entry_status_as_guest ]]")

        url = f'/api/member_status/'
        token = self.guest_user_token
        response = self.client.get(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }

        expected_response = [
            {
                'member_id': self.member.member_id,
                'guest_name': self.guest_member.user_name,
                'member_status': self.member.member_status,
                'list_id': self.list_instance.list_id,
                'list_name': self.list_instance.list_name,
                'owner_name': self.list_owner.user_name,
                'is_owner': False,
            }
        ]
        response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # ゲストでもオーナーでもないユーザーがリクエスト、空のレスポンスを期待
    def test_get_entry_status_as_another_user(self):
        print("\n[[ EntryMemberStatusViewTestCase/test_get_entry_status_as_another_user ]]")

        url = f'/api/member_status/'
        token = self.another_user_token
        response = self.client.get(url, format='json', HTTP_COOKIE=f"jwt_token={str(token)}")
        headers = {
            "Cookie": f"jwt_token={str(token)}"
        }

        expected_response = []

        response = response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)

    # 認証されていないユーザーがアクセス　401エラーが期待される
    def test_get_entry_status_unauthenticated(self):
        print("\n[[ EntryMemberStatusViewTestCase/test_get_entry_status_unauthenticated ]]")

        url = f'/api/member_status/'   
        invalid_token = "invalid_token_value"
        response = self.client.get(url, format='json', HTTP_COOKIE=f"jwt_token={str(invalid_token)}")
        headers = {
            "Cookie": f"jwt_token={str(invalid_token)}"
        }
    
        expected_response =  {'detail': 'トークンが無効です'}

        response = response = self.client.get(url, headers=headers, format='json')

        # HTTPステータスコードの確認
        print('[Result]: ', response.status_code, '==', status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # レスポンスデータの確認
        print('[Result]: ', response.data)
        print('[Expect]: ', expected_response)
        self.assertEqual(response.data, expected_response)
        




    
