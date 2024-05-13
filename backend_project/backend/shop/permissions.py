from rest_framework import permissions

# リストのオーナーのみ許可
class IsOwner(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        return list_instance.owner_id == request.user

# リストのオーナーと招待者許可
class IsOwnerOrInvitee(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user
        # 招待者であるかどうかチェック
        invitee_check = list_instance.members.filter(guest_id=request.user, member_status=0).exists()

        return owner_check or invitee_check  
   

# リストのオーナーと編集権限を持つ招待者許可
class IsOwnerOrInviteeWithAuthority(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user
        # 招待者であるかどうかチェック
        invitee_check = list_instance.members.filter(guest_id=request.user, authority=True, member_status=0).exists()

        return owner_check or invitee_check  
   


