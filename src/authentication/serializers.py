from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Inscription : password en write_only + validate_age (RGPD ≥ 15) + hash via create_user."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        read_only_fields = ["id"]

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("RGPD : l'inscription est interdite aux moins de 15 ans.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """CRUD du profil utilisateur (lecture / mise à jour / suppression)."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "date_joined"]
