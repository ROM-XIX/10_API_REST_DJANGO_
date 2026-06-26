from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Contributor, Project


class ProjectListSerializer(serializers.ModelSerializer):
    """Liste légère : id, title, type, author_id, created_time (Green Code)."""

    class Meta:
        model = Project
        fields = ["id", "title", "type", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Détail enrichi : auteur et contributeurs nested (1 niveau, max CDC)."""

    author = UserSerializer(read_only=True)
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "contributors",
            "created_time",
        ]
        read_only_fields = ["id", "author", "contributors", "created_time"]

    def get_contributors(self, obj):
        # select_related évite N+1 (M2 Sq6 + CDC Green Code)
        users = [c.user for c in obj.contributors.all().select_related("user")]
        return UserSerializer(users, many=True).data


class ContributorSerializer(serializers.ModelSerializer):
    """Gestion d'un contributeur : ajouté via /projects/{id}/users/."""

    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]
        read_only_fields = ["id", "project"]
