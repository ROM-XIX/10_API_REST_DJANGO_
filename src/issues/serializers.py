from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Issue


class IssueListSerializer(serializers.ModelSerializer):
    """Liste légère : id, title, tag, priority, status, author_id, assignee_id, created_time."""

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "created_time",
        ]
        read_only_fields = ["id", "author", "created_time"]


class IssueDetailSerializer(serializers.ModelSerializer):
    """Détail enrichi : description + project + auteur nested (1 niveau, Green Code)."""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "project",
            "author",
            "assignee",
            "created_time",
        ]
        read_only_fields = ["id", "project", "author", "created_time"]
