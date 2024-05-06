from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shop.views import items_views, user, login, line

urlpatterns = [
    path('items/<str:user_id>/<int:list_id>', items_views.ItemList.as_view()),
]

urlpatterns += [
    path('user/', user.UserView.as_view(), name='user'),
    path('login/', login.LoginView.as_view(), name='login'),
    path('callback/', line.LineCallbackView.as_view(),
         name='line-callback'),
    path('line/', line.LineSignupView.as_view(), name='line-signup'),
    path('line-login/', line.LineLoginView.as_view(), name='line-login')
]
urlpatterns = format_suffix_patterns(urlpatterns)
