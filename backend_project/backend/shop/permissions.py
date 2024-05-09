from rest_framework import permissions

# リストのオーナーのみ許可
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, list_instance):
        return list_instance.owner_id == request.user.user_id

# リストのオーナーと招待者許可
class IsOwnerOrInvitee(permissions.BasePermission):

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user.user_id
        # 招待者であるかどうかチェック
        invitee_check = list_instance.members.filter(invitee_id=request.user.user_id).exists()

        return owner_check or invitee_check  
   

# リストのオーナーと編集権限を持つ招待者許可
class IsOwnerOrInviteeWithAuthority(permissions.BasePermission):

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user.user_id
        # 招待者であるかどうかチェック
        invitee_check = list_instance.members.filter(invitee_id=request.user.user_id, authority=True).exists()

        return owner_check or invitee_check  
   


