from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    *router.urls,
]
