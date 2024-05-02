from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items_views, user, login

urlpatterns = [
    path('shop/items/<str:user_id>/<int:list_id>', items_views.ItemList.as_view()),
]

urlpatterns += [
    path('api/user/', user.UserView.as_view(), name='user'),
    path('api/login/', login.LoginView.as_view(), name='login')
]
urlpatterns = format_suffix_patterns(urlpatterns)
