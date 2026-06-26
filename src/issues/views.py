from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from projects.models import Project

from .models import Issue
from .serializers import IssueDetailSerializer, IssueListSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """CRUD des issues d'un projet : /projects/{project_pk}/issues/."""

    def get_queryset(self):
        return (
            Issue.objects.filter(
                project_id=self.kwargs["project_pk"],
                project__contributors__user=self.request.user,
            )
            .select_related("author", "assignee", "project")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == "list":
            return IssueListSerializer
        return IssueDetailSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            pk=self.kwargs["project_pk"],
            contributors__user=self.request.user,
        )
        serializer.save(author=self.request.user, project=project)
