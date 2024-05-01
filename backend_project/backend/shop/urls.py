from django.urls import path
from shop.views import items_views

urlpatterns = [
    path('api/items/<user_id>/<list_id>/', items_views.ItemList.as_view()),


]

