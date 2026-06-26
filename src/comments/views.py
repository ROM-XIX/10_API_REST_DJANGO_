from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from issues.models import Issue

from .models import Comment
from .serializers import CommentDetailSerializer, CommentListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD des comments d'une issue : /projects/{project_pk}/issues/{issue_pk}/comments/."""

    lookup_field = "uuid"

    def get_queryset(self):
        return (
            Comment.objects.filter(
                issue_id=self.kwargs["issue_pk"],
                issue__project_id=self.kwargs["project_pk"],
                issue__project__contributors__user=self.request.user,
            )
            .select_related("author", "issue", "issue__project")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return CommentDetailSerializer

    def perform_create(self, serializer):
        issue = get_object_or_404(
            Issue,
            pk=self.kwargs["issue_pk"],
            project_id=self.kwargs["project_pk"],
            project__contributors__user=self.request.user,
        )
        serializer.save(author=self.request.user, issue=issue)
