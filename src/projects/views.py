from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Contributor, Project
from .serializers import (
    ContributorSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD projets : un user voit uniquement ceux où il contribue."""

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user).select_related("author").distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """Gestion des contributeurs d'un projet : /projects/{project_pk}/users/."""

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"]).select_related("user", "project")

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(project=project)
