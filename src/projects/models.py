from django.conf import settings
from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=ProjectType.choices)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )

    class Meta:
        unique_together = ("user", "project")
        ordering = ["id"]

    def __str__(self):
        return f"{self.user} → {self.project}"
