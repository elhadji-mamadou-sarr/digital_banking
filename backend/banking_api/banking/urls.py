from django.urls import path
from .views import (DetailApiView, CreateApiView, UpdateApiView, 
                    DeleteApiView, ListAccountView)
from banking_inscription.views import (UserListView,
                                       UserCreateView, UserDetailView,
                                       UserUpdateView, UserDeleteView)

from banking_inscription.views import inactive_users_view

from .deposit_view import deposit_view
from .withdrawl_view import withdraw_view


urlpatterns = [
    
   # path('', comptes_view, name='comptes_view'),
    path('', ListAccountView.as_view()),
    path('<int:pk>', DetailApiView.as_view()),
    path('create', CreateApiView.as_view()),
    path('<int:pk>', UpdateApiView.as_view()),
    path('delete/<int:pk>', DeleteApiView.as_view()),

    path('users', UserListView.as_view()),
    path('users/create', UserCreateView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('update/<int:pk>', UserUpdateView.as_view()),
    path('users/delete/<int:pk>', UserDeleteView.as_view()),
    path('inactive_users/', inactive_users_view, name='inactive_users'),
    
    path('<int:pk>/deposit', deposit_view),
    path('<int:pk>/withdraw', withdraw_view),
]
