from rest_framework import permissions

# リストのオーナーのみ許可
class IsOwner(permissions.BasePermission):

    def has_object_permissions(self, request, view, obj):
        return obj.owner_id == request.user.user_id

# リストのオーナーと招待者許可
class IsOwnerOrInvitee(permissions.BasePermission):

# リストのオーナーと編集権限を持つ招待者許可
class IsOwnerOrInviteeWithAuthority(permissions.BasePermission):

