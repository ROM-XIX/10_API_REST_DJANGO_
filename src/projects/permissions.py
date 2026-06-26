from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Project


class IsAuthorOrReadOnly(BasePermission):
    """Lecture autorisée à tout user qui passe has_permission.
    Écriture/suppression uniquement par l'auteur de l'objet (champ `author`).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """Lecture libre pour les contributeurs du projet (filtrée par le queryset).
    Écriture (ajout/suppression de contributeurs) uniquement par l'auteur du projet.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        project_pk = view.kwargs.get("project_pk")
        if not project_pk:
            return False
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            return False
        return project.author == request.user
