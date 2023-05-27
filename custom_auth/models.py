from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import UserManager

from datetime import timedelta


def get_future():
    return timezone.now() + timedelta(hours=72)


class CustomUserManager(UserManager):
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, email, password, **extra_fields)


class User(AbstractUser):
    phone = models.CharField(
        max_length=12,
        verbose_name='Телефон',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=False
    )
    activation_code = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Код активации'
    )
    activation_code_expires = models.DateTimeField(
        default=get_future
    )
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.email
    
    @property
    def is_activation_code_expired(self):
        return timezone.now() > self.activation_code_expires
