from django.contrib.auth.models import AbstractUser
from django.db import models

import users.constants as cnst


class User(AbstractUser):
    CHOICES = (
        (cnst.ROLE_USER, cnst.ROLE_USER),
        (cnst.ROLE_MODERATOR, cnst.ROLE_MODERATOR),
        (cnst.ROLE_ADMIN, cnst.ROLE_ADMIN),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=cnst.ROLE_USER
    )
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def is_admin(self):
        return self.role == cnst.ROLE_ADMIN

    def is_moderator(self):
        return self.role == cnst.ROLE_MODERATOR

    def is_user(self):
        return self.role == cnst.ROLE_USER

    def __str__(self):
        return self.username
