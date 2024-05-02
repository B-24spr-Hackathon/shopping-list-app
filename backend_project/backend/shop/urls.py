from django.urls import path
from shop.views import items_views

urlpatterns = [
     # アイテムリスト表示、アイテム作成
    path('api/items/<user_id>/<list_id>/', items_views.ItemList.as_view()),
     # アイテム更新
    path('api/items/<user_id>/<item_id>/', items_views.ItemUpdate.as_view()),
]

