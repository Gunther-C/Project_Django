from django.urls import path
from .views import registration, connection
from .views import UserPasswordChangeView, UserEmailChangeView


urlpatterns = [
    path('', connection, name='login'),
    path('registration/', registration, name='registration'),
    path('password_change/', UserPasswordChangeView.as_view(), name='chg-password'),
    path('email_change/', UserEmailChangeView.as_view(), name='chg-email')
]
