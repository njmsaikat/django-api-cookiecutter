from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("user_type", User.UserType.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Project user. `user_type` is embedded in the JWT as a claim; views branch on it to scope
    querysets per role (see utils.utils.get_user_type and example.views).
    """

    class UserType(models.TextChoices):
        ADMIN = "admin", "Admin"
        OPERATION = "operation", "Operation"
        AUTHOR = "author", "Author"
        USER = "user", "User"

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.USER, db_index=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
