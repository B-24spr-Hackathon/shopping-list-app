from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items_views

urlpatterns = [
    path('shop/items/<str:user_id>/<int:list_id>', items_views.ItemList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
