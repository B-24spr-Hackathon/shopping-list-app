from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import (
    items, user, login, line, lists, healthcheck, webhook, shoppinglist, invite, entry, apply,
)

urlpatterns = [
    # アイテムリスト表示GET、アイテム作成POST
    path('items/<list_id>/', items.ItemCreateView.as_view(),name="item-post-get"),
    # アイテム更新PATCH、削除DELETE
    path('items/<list_id>/<item_id>/', items.ItemDetailView.as_view(), name="item-patch-delete"),
    # 買い物リスト表示GET
    path('shopping-list/<list_id>/', shoppinglist.ShoppingListView.as_view(), name="shoppinglist"),
    # リスト設定（登録）POST
    path('list/', lists.ListView.as_view(), name="list-post"),
    # リスト設定（表示）GET,（更新）PATCH, (削除）DELETE
    path('list/<list_id>/', lists.ListView.as_view(), name="list-get-patch-delete"),
    # 招待機能 GET
    path('invite/<user_id>/', invite.InviteView.as_view(), name="find-invitee-get"),
    # 招待機能 POST
    path('invite/', invite.InviteView.as_view(), name="invitee-post"),
    # 招待/申請機能 PATCH, DELETE
    path('entry/<member_id>/', entry.EntryView.as_view(), name="entry-patch-delete"),
    # 招待/申請機能 承認PATCH
    path('entry/accept/<member_id>/', entry.EntryAcceptView.as_view(), name="accept"),
    # 招待/申請機能 拒否DELETE
    path('entry/decline/<member_id>/', entry.EntryDeclineView.as_view(), name="decline"),
    # 申請機能 GET
    path('apply/<user_id>/', apply.ApplyView.as_view(), name="apply-get"),
    # 申請機能 POST
    path('apply/', apply.ApplyView.as_view(), name="apply-post"),
    # 招待・申請状況確認 GET
    path('entry/member_status/<user_id>/', entry.EntryAcceptView.as_view(), name='entry-status'),
]

urlpatterns += [
    path("", healthcheck.HealthcheckView.as_view(), name="healthcheck"),
    path("user/", user.UserView.as_view(), name="user"),
    path("login/", login.LoginView.as_view(), name="login"),
    path("callback/", line.LineCallbackView.as_view(),
         name="line-callback"),
    path("line/", line.LineSignupView.as_view(), name="line-signup"),
    path("line-login/", line.LineLoginView.as_view(), name="line-login"),
    path("line-link/", line.LineLinkView.as_view(), name='line-link'),
    path("line-webhook/", webhook.LineWebhookView.as_view(),
         name="line-webhook")
]
urlpatterns = format_suffix_patterns(urlpatterns)
