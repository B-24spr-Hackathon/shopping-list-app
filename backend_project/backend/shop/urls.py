from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items, user, login, line, lists, healthcheck, webhook

urlpatterns = [
    # アイテムリスト表示GET、アイテム作成POST
    path('api/items/<list_id>/', items.ItemView.as_view()),
    # アイテム更新PATCH、削除DELETE
    path('api/items/<item_id>/', items.ItemView.as_view()),
    # 買い物リスト表示GET
    path('api/shopping-list/<list_id>/', lists.ListView.as_view()),
    # リスト設定（登録）POST
    path('api/list/', lists.ListView.as_view()),
    # リスト設定（表示）GET,（更新）PATCH, (削除）DELETE
    path('api/list/<list_id>/', lists.ListView.as_view()),

]

urlpatterns += [
    path("api/", healthcheck.HealthcheckView.as_view(), name="healthcheck"),
    path("api/user/", user.UserView.as_view(), name="user"),
    path("api/login/", login.LoginView.as_view(), name="login"),
    path("api/callback/", line.LineCallbackView.as_view(),
         name="line-callback"),
    path("api/line/", line.LineSignupView.as_view(), name="line-signup"),
    path("api/line-login/", line.LineLoginView.as_view(), name="line-login"),
    path("api/line-link/", line.LineLinkView.as_view(), name='line-link'),
    path("api/line-webhook/", webhook.LineWebhookView.as_view(),
         name="line-webhook")
]
urlpatterns = format_suffix_patterns(urlpatterns)
