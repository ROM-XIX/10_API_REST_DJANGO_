from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """Liste légère : uuid, description, author_id, created_time."""

    class Meta:
        model = Comment
        fields = ["uuid", "description", "author", "created_time"]
        read_only_fields = ["uuid", "author", "created_time"]


class CommentDetailSerializer(serializers.ModelSerializer):
    """Détail enrichi : auteur nested (1 niveau)."""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["uuid", "description", "issue", "author", "created_time"]
        read_only_fields = ["uuid", "issue", "author", "created_time"]
