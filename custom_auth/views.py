from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .forms import UserRegisterForm, UserLoginForm
from .models import User


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                send_verify_email(user)
            return redirect('main:main')
        else:
            return render(request, 'custom_auth/register.html', {'form': form})
    elif request.method == 'GET':
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'custom_auth/register.html', context)
    

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'custom_auth/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:main'))


def send_verify_email(user):
    """
    отправка письма пользователю с подтверждением
    """
    if user.is_active:
        # пользователь уже активен
        return None
    params = {
        'email': user.email,
        'activation_code': user.activation_code
    }
    link = reverse('auth:verify', kwargs=params)
    title = f'Подтверждение {user.email}'
    body = f'Для активации перейдите по ссылке http://192.168.0.59:8000{link}'
    send_mail(title, body, settings.DEFAULT_FROM_EMAIL, [user.email])


def verify_user(request, email, activation_code):
    try:
        user = User.objects.get(email=email, activation_code=activation_code)
        if not user.is_activation_code_expired:
            user.is_active = True
            user.save()
            login(request, user)
        return HttpResponseRedirect(reverse('main:main'))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('main:main'))