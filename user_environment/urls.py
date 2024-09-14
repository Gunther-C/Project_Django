from django.urls import path

from .views import UserFluxView, UserPostView, UserFollowView
from .views import TicketCreateView, ReviewCreateView, FollowCreateView, ReviewResponseCreateView
from .views import TicketUpdateView, ReviewUpdateView
from .views import TicketDeleteView, ReviewDeleteView, FollowDeleteView
from .views import searching

urlpatterns = [
    path('user_flux/', UserFluxView.as_view(), name='user-flux'),
    path('user_posts/', UserPostView.as_view(), name='user-posts'),
    path('user_follows/', UserFollowView.as_view(), name='user-follows'),
    path('create_ticket/', TicketCreateView.as_view(), name='crt-ticket'),
    path('create_review/', ReviewCreateView.as_view(), name='crt-review'),
    path('create_follow/<int:pk>/', FollowCreateView.as_view(), name='crt-follow'),
    path('response_review/<int:pk>/', ReviewResponseCreateView.as_view(), name='crt-rsp-review'),
    path('update_ticket/<int:pk>/', TicketUpdateView.as_view(), name='upd-ticket'),
    path('update_review/<int:pk>/', ReviewUpdateView.as_view(), name='upd-review'),
    path('delete_ticket/<int:pk>/', TicketDeleteView.as_view(), name='del-ticket'),
    path('delete_review/<int:pk>/', ReviewDeleteView.as_view(), name='del-review'),
    path('delete_follow/<int:pk>/', FollowDeleteView.as_view(), name='del-follow'),
    path('searching/', searching, name='search'),
]
