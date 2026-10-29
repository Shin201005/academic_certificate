
from django.urls import path

from .views import (
    LoginView,
    MeView,
    RefreshView,
    LogoutView,
    AdminOnlyView,
    SchoolOnlyView,
    StudentOnlyView,
    csrf_view,
)

urlpatterns = [
    path("csrf/", csrf_view, name="api_csrf"),
    path("login/", LoginView.as_view(), name="api_login"),
    path("me/", MeView.as_view(), name="api_me"),
    path("refresh/", RefreshView.as_view(), name="api_refresh"),
    path("logout/", LogoutView.as_view(), name="api_logout"),

    path("admin-only/", AdminOnlyView.as_view(), name="api_admin_only"),
    path("school-only/", SchoolOnlyView.as_view(), name="api_school_only"),
    path("student-only/", StudentOnlyView.as_view(), name="api_student_only"),
]
