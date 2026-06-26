"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from comments.views import CommentViewSet
from issues.views import IssueViewSet
from projects.views import ContributorViewSet, ProjectViewSet

# Router principal — /api/projects/
projects_root_router = DefaultRouter()
projects_root_router.register("projects", ProjectViewSet, basename="project")

# Router imbriqué — /api/projects/{project_pk}/(users|issues)/
projects_nested_router = NestedDefaultRouter(projects_root_router, "projects", lookup="project")
projects_nested_router.register("users", ContributorViewSet, basename="project-users")
projects_nested_router.register("issues", IssueViewSet, basename="project-issues")

# Router doublement imbriqué — /api/projects/{project_pk}/issues/{issue_pk}/comments/
issues_nested_router = NestedDefaultRouter(projects_nested_router, "issues", lookup="issue")
issues_nested_router.register("comments", CommentViewSet, basename="issue-comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT (simplejwt)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # App authentication (register + users CRUD)
    path("api/", include("authentication.urls")),
    # Apps projects + issues + comments (CRUD + nested 2 niveaux)
    path("api/", include(projects_root_router.urls)),
    path("api/", include(projects_nested_router.urls)),
    path("api/", include(issues_nested_router.urls)),
]
