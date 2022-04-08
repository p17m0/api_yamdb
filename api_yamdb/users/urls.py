from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, users_login, users_login_token

router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('auth/signup/', users_login, name='user_signup'),
    path('auth/token/', users_login_token, name='user_token'),
    path(
        'users/me/',
        UserViewSet.as_view({'patch': 'get_me',
                             'get': 'get_me',
                             'delete': 'get_me'}), name='user_me'),
    path('', include(router.urls)),
]
