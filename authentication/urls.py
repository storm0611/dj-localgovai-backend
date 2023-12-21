from django.urls import path, re_path
from .views import (
    LoginView,
    RegisterView,
    UserView,
    PasswordResetView,
    UserSearchView
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('user', UserView.as_view(), name='user'),
    path('user/search', UserSearchView.as_view(), name='user_search'),
    path('send-reset-link', PasswordResetView.as_view(), name='send_reset_link'),
    path('confirm/<uidb64>/<token>', PasswordResetView.as_view(), name='confirm'),
    path('reset-password', PasswordResetView.as_view(), name='reset_password'),
]
