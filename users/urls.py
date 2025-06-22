from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'auth',views.AuthViewSet, basename='auth')
router.register(r'sub_schools',views.SubSchoolViewSet,basename='sub_schools')
router.register(r'users',views.UserViewSet,basename='users')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/token/refresh',TokenRefreshView.as_view(),name='token_refresh')
]



# This will generate the following URLs automatically:
# GET    /api/auth/                     -> List auth actions (not used, but available)
# POST   /api/auth/register/            -> Register new user
# POST   /api/auth/login/               -> Login user
# POST   /api/auth/logout/              -> Logout user
# GET    /api/auth/profile/             -> Get user profile
# PUT    /api/auth/update_profile/      -> Update user profile
# PATCH  /api/auth/update_profile/      -> Partially update user profile
# POST   /api/auth/change_password/     -> Change password
#
# GET    /api/users/                    -> List all users (admin only)
# POST   /api/users/                    -> Create user (admin only)
# GET    /api/users/{id}/               -> Get specific user
# PUT    /api/users/{id}/               -> Update specific user
# PATCH  /api/users/{id}/               -> Partially update specific user
# DELETE /api/users/{id}/               -> Delete user (admin only)
# POST   /api/users/{id}/set_password/  -> Set user password (admin only)