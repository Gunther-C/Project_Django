from django.urls import path
from .views import registration, connection

# app_name = 'auth'

urlpatterns = [
    path('', connection, name='login'),
    path('registration/', registration, name='registration'),
]
