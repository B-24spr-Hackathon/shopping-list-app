from rest_framework import permissions
import logging

logger = logging.getLogger("backend")


# リストのオーナーのみ許可
class IsOwner(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        if list_instance.owner_id != request.user:
            logger.error(f"IsOwner: {self.message}")
        else:
            logger.info("IsOwner: 権限有り")
        return list_instance.owner_id == request.user

# リストのオーナーとゲスト許可
class IsOwnerOrGuest(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user
        # ゲストであるかどうかチェック
        guest_check = list_instance.members.filter(guest_id=request.user, member_status=0).exists()
        
        if not owner_check and not guest_check:
            logger.error(f"IsOwnerOrGuest: {self.message}")
        else:
            logger.info("IsOwnerOrGuest: 権限有り")

        return owner_check or guest_check


# リストのオーナーと編集権限を持つゲスト許可
class IsOwnerOrGuestWithAuthority(permissions.BasePermission):
    message ='アクセスする権限がありません'

    def has_object_permission(self, request, view, list_instance):
        # オブジェクトのオーナーであるかどうかチェック
        owner_check = list_instance.owner_id == request.user
        # ゲストであるかどうかチェック
        guest_check = list_instance.members.filter(guest_id=request.user, authority=True, member_status=0).exists()

        if not owner_check and not guest_check:
            logger.error(f"IsOwnerOrGuestWithAuthority: {self.message}")
        else:
            logger.info("IsOwnerOrGuestWithAuthority: 権限有り")

        return owner_check or guest_check