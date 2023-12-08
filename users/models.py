from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    class TeamChoices(models.TextChoices):
        Danbi = "Danbi", "단비"
        Darae = "Darae", "다래"
        Blahblah = "BlahBlah", "블라블라"
        Cheolro = "Cheolro", "철로"
        Ddange = "Ddange", "땅이"
        Haetae = "Haetae", "해태"
        Supie = "Supie", "수피"

    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    team = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
        default=TeamChoices.Danbi,
    )

    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
