from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import PublicSchoolViewSet

router = DefaultRouter()

router.register(r'schools', views.SchoolViewSet,basename='schools')
router.register(r'departments',views.SubSchoolViewSet,basename='departments')
router.register(r'public/schools',views.PublicSchoolViewSet,basename='public-schools')

urlpatterns = [
    path('',include(router.urls))
]

# This generates:
# GET    /api/schools/                     -> List schools (filtered by user)
# POST   /api/schools/                     -> Create school (super admin only)
# GET    /api/schools/{id}/                -> Get school details
# PUT    /api/schools/{id}/                -> Update school
# DELETE /api/schools/{id}/                -> Delete school (super admin only)
# GET    /api/schools/{id}/users/          -> List users in school
# GET    /api/schools/{id}/departments/    -> List departments in school
# POST   /api/schools/{id}/toggle_status/  -> Toggle school status

# GET    /api/departments/                 -> List departments (filtered by user's school)
# POST   /api/departments/                 -> Create department
# GET    /api/departments/{id}/            -> Get department details
# PUT    /api/departments/{id}/            -> Update department
# DELETE /api/departments/{id}/            -> Delete department
# GET    /api/departments/{id}/users/      -> List users in department

# GET    /api/public/schools/              -> Public list of active schools
# GET    /api/public/schools/by_domain/?domain=example.edu -> Find school by domain