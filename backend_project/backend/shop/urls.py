from django.urls import path
from shop.views import items_views
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items, signup

urlpatterns = [
     # アイテムリスト表示、アイテム作成
    path('api/items/<user_id>/<list_id>/', items.ItemList.as_view()),
     # アイテム更新
    path('api/items/<user_id>/<item_id>/', items.ItemUpdate.as_view()),
]

urlpatterns += [
    path('api/user/', signup.SignupView.as_view(), name='signup')
]
urlpatterns = format_suffix_patterns(urlpatterns)
