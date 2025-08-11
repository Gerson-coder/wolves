from django.urls import path
from . import views

urlpatterns = [
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('logout_usuario/', views.logout_usuario, name='logout_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar-avatar/', views.cambiar_avatar, name='cambiar_avatar'),
    path('detalle_jugador/<str:username>/', views.perfil_usuario, name='detalle_jugador'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('jugadores/', views.jugadores, name='jugadores'),
]

