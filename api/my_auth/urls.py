from django.urls import path
from .views import (
    LoginApiView,
    LogoutApiView,
    UserProfileApiView,
    RegisterApiView,
    TokenRefreshApiView,
)

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('refresh/', TokenRefreshApiView.as_view(), name='token_refresh'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('me/', UserProfileApiView.as_view(), name='user_profile'),
]
