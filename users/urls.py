from django.urls import path
from . import views

urlpatterns = [
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
]

