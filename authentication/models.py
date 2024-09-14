from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    # username = None
    email = models.EmailField(validators=[validate_email], unique=True)
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
