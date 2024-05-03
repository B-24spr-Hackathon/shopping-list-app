from django.urls import path
from shop.views import items
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items, user, login

urlpatterns = [
     # アイテムリスト表示GET、アイテム作成POST
    path('api/items/<user_id>/<list_id>/', items.ItemView.as_view()),
     # アイテム更新PATCH、削除DELETE
    path('api/items/<user_id>/<item_id>/', items.ItemView.as_view()),
]

urlpatterns += [
    path('api/user/', user.UserView.as_view(), name='user'),
    path('api/login/', login.LoginView.as_view(), name='login')
]
urlpatterns = format_suffix_patterns(urlpatterns)
