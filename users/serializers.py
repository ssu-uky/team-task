import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "team"]

    def validate_username(self, value):
        if not re.match(r"^[a-zA-Z0-9_]{4,16}$", value):
            raise ValidationError(
                "Username must be between 4 and 16 characters long and can only contain letters, numbers and underscores."
            )
        return value

    def validate_password(self, password):
        if not re.match(r"^[a-zA-Z0-9_]{8,16}$", password):
            raise ValidationError(
                "Password must be between 8 and 16 characters long and can only contain letters, numbers and underscores."
            )
        return make_password(password)
