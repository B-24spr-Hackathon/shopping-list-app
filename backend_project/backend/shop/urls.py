from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items, user, login, lists

urlpatterns = [
    # アイテムリスト表示GET、アイテム作成POST
    path('api/items/<user_id>/<list_id>/', items.ItemView.as_view()),
    # アイテム更新PATCH、削除DELETE
    path('api/items/<user_id>/<item_id>/', items.ItemView.as_view()),
    # 買い物リスト表示GET
    path('api/shopping-list/<list_id>/', lists.ListView.as_view())
]

urlpatterns += [
    path('api/user/', user.UserView.as_view(), name='user'),
    path('api/login/', login.LoginView.as_view(), name='login')
]
urlpatterns = format_suffix_patterns(urlpatterns)
