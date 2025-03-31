from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Especifica los related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_wolves_set',  # Nombre personalizado para evitar conflictos
        related_query_name='user_wolves',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_wolves_set',  # Nombre personalizado para evitar conflictos
        related_query_name='user_wolves',
    )
    
    nickname = models.CharField('Nickname', max_length=50, null=False, blank=False, unique=True)
    lv = models.PositiveIntegerField('Nivel', blank=False, null=False, default=1)
    nombre = models.CharField('Nombre', max_length=50, blank=False, null=False)
    edad = models.PositiveIntegerField('Edad', blank=False, null=False)
    pais = models.CharField('País', max_length=50, blank=False, null=False)
    ciudad = models.CharField('Ciudad', max_length=50, blank=False, null=False)
    estadoCpl = models.CharField('Estado de cpl', max_length=50, blank=True, null=True)
    hobby = models.CharField('Pasatiempo', max_length=50, blank=False, null=False)
    fechaCumpleaños = models.DateField('Fecha de cumpleaños', blank=True, null=True)
    puntos = models.PositiveIntegerField('Puntos de honor', default=0, blank=False, help_text='ganados en eventos de clan')
    mododeJuego = models.CharField('Modo que mas juegas', max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f'nickname {self.nickname}- nombre: {self.nombre}'