from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('verify/<str:email>/<str:activation_code>', views.verify_user, name='verify'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]