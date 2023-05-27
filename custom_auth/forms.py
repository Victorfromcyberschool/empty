import random
import hashlib

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        activation_code = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.activation_code = activation_code
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    pass
