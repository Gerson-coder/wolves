from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import math

# Definición de rangos del clan
RANKS = [
    ('RECLUTA', 'Recluta'),
    ('MEMBER', 'Miembro'),
    ('VETERAN', 'Veterano'),
    ('ELITE', 'Élite'),
    ('MASTER', 'Maestro'),
    ('LEGEND', 'Leyenda'),
]

# Roles especiales
SPECIAL_ROLES = [
    ('ADMIN', 'Administrador'),
    ('NONE', 'Ninguno'),
    ('SUBLEADER', 'Sublíder'),
    ('CAPTAIN', 'Capitán de Equipo'),
    ('TRAINER', 'Entrenador'),
    ('EVENT_MANAGER', 'Gestor de Eventos'),
    ('CONTENT_CREATOR', 'Creador de Contenido'),
    ('MODERATOR', 'Moderador'),
   
    ('AMATEUR', 'Cahorro'),
  
]

# Especialidades/habilidades principales
SPECIALTIES = [
    ('R', 'Todoterreno'),
    ('STRATEGIST', 'Estratega'),
    ('SUPPORT', 'Soporte'),
    ('FRAGGER', 'Fragger'),
    ('SNIPER', 'Francotirador'),
    ('LEADER', 'Líder'),
    ('SPEEDRUNNER', 'Speedrunner'),
    ('COLLECTOR', 'Coleccionista'),
]

class Create_subs(models.Model):
    nombre = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True, help_text="Descripción del equipo o grupo")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    members_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Sublíder'
        verbose_name_plural = 'Sublíderes'

    def __str__(self):
        return self.nickname if self.nickname else "Subs sin nickname"

class CreateUser(AbstractUser):
    nombre = models.CharField(max_length=20, blank=True)
    edad = models.PositiveIntegerField(null=True)
    nickname = models.CharField(max_length=100, null=True)
    cumpleaños = models.DateTimeField(null=True)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    hobby = models.CharField(max_length=20, blank=True)
    estado_cpl = models.CharField(max_length=100)
    juego_principal = models.CharField(max_length=100, blank=True, null=True)
    modo_de_juego = models.CharField(max_length=100)
    reclutado_por = models.ForeignKey('Create_subs', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_subleader = models.BooleanField(default=False)
    
    # Nuevos campos
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="Cuéntanos sobre ti")
    discord_id = models.CharField(max_length=100, blank=True, null=True)
    twitch_username = models.CharField(max_length=100, blank=True, null=True)
    youtube_channel = models.CharField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    juego_principal = models.CharField(max_length=100, blank=True, null=True)
    streaming_enabled = models.BooleanField(default=False, help_text="¿Haces streaming de tus partidas?")
    last_active = models.DateTimeField(auto_now=True)
    
    # Configuración de privacidad
    show_email = models.BooleanField(default=False)
    show_discord = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username and self.nickname:
            self.username = self.nickname
            
        # Crear perfil automáticamente si no existe
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            Perfil.objects.create(
                user=self,
                nickname=self.nickname,
                nivel=1,
                puntos_exp=0,
                puntos_honor=0,
                xp_siguiente_nivel=100
            )

class Perfil(models.Model):
    user = models.OneToOneField(CreateUser, on_delete=models.CASCADE, related_name='perfil')
    nickname = models.CharField(max_length=100, null=True)
    
    # Sistema de niveles y puntos
    nivel = models.PositiveIntegerField(default=1)
    puntos_exp = models.PositiveIntegerField(default=0)
    puntos_honor = models.PositiveIntegerField(default=0)
    xp_siguiente_nivel = models.PositiveIntegerField(default=100)
    
    # Nuevos campos para el sistema de rango y roles
    rango = models.CharField(max_length=20, choices=RANKS, default='Recluta')
    rol_especial = models.CharField(max_length=20, choices=SPECIAL_ROLES, default='Ninguno')
    especialidad = models.CharField(max_length=20, choices=SPECIALTIES, default='Todoterreno')
    
    # Estadísticas de participación
    torneos_participados = models.PositiveIntegerField(default=0)
    torneos_ganados = models.PositiveIntegerField(default=0)
    eventos_asistidos = models.PositiveIntegerField(default=0)
    misiones_completadas = models.PositiveIntegerField(default=0)
    fecha_ultimo_ascenso = models.DateTimeField(null=True, blank=True)
    dias_en_clan = models.PositiveIntegerField(default=0)
    
    # Sistema de actividad
    actividad_semanal = models.PositiveIntegerField(default=0)
    ultima_actividad = models.DateTimeField(null=True, blank=True)
    estado_actividad = models.CharField(max_length=20, default='ONLINE', 
                                       choices=[('ONLINE', 'En línea'), ('AWAY', 'Ausente'), 
                                                ('BUSY', 'Ocupado'), ('OFFLINE', 'Desconectado')])
    
    # Campo para un mensaje personalizado
    mensaje_estado = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.nickname if self.nickname else "Perfil sin nickname"
    
    def add_exp(self, amount):
        """Añadir experiencia y subir de nivel si es necesario"""
        self.puntos_exp += amount
        
        # Verificar si debe subir de nivel
        while self.puntos_exp >= self.xp_siguiente_nivel:
            self.nivel_up()
            
        self.save()
    
    def nivel_up(self):
        """Subir de nivel al perfil del usuario"""
        self.nivel += 1
        self.puntos_exp -= self.xp_siguiente_nivel
        
        # La fórmula hace que cada nivel requiera más XP (curva de dificultad)
        self.xp_siguiente_nivel = int(100 * math.pow(1.2, self.nivel))
        
        # Notificar al usuario y otorgar recompensas por subir de nivel
        Notificacion.objects.create(
            user=self.user,
            tipo='LEVEL_UP',
            mensaje=f'¡Felicidades! Has alcanzado el nivel {self.nivel}.'
        )
        
        # Actualizar rango si corresponde
        self.check_rank_promotion()
        
    def check_rank_promotion(self):
        print(f"Nivel actual: {self.nivel}, Rango actual: {self.rango}")
        """Verificar si el usuario merece una promoción de rango"""
        # Lógica de promoción basada en nivel
        if self.nivel >= 50 and self.rango != 'LEGEND':
            self.rango = 'LEGEND'
            self.fecha_ultimo_ascenso = timezone.now()
        elif self.nivel >= 40 and self.rango != 'MASTER' and self.rango != 'LEGEND':
            self.rango = 'MASTER'
            self.fecha_ultimo_ascenso = timezone.now()
        elif self.nivel >= 30 and self.rango not in ['ELITE', 'MASTER', 'LEGEND']:
            self.rango = 'ELITE'
            self.fecha_ultimo_ascenso = timezone.now()
        elif self.nivel >= 20 and self.rango not in ['VETERAN', 'ELITE', 'MASTER', 'LEGEND']:
            self.rango = 'VETERAN'
            self.fecha_ultimo_ascenso = timezone.now()
        elif self.nivel >= 10 and self.rango == 'Recluta':
            self.rango = 'Miembro'
            self.fecha_ultimo_ascenso = timezone.now()
            
        # Notificar si hubo promoción
        if self.fecha_ultimo_ascenso and self.fecha_ultimo_ascenso.date() == timezone.now().date():
            Notificacion.objects.create(
                user=self.user,
                tipo='RANK_UP',
                mensaje=f'¡Felicidades! Has sido promovido al rango de {self.get_rango_display()}.'
            )
            
    def get_progress_percent(self):
        """Obtener el porcentaje de progreso hacia el siguiente nivel"""
        return int((self.puntos_exp / self.xp_siguiente_nivel) * 100)
    
    def actualizar_dias_clan(self):
        """Actualizar los días que el usuario ha estado en el clan"""
        dias = (timezone.now().date() - self.user.date_joined.date()).days
        self.dias_en_clan = dias
        self.save()
    
    def update_activity(self):
        """Actualizar la última actividad del usuario"""
        self.ultima_actividad = timezone.now()
        self.actividad_semanal += 1
        self.save()

# Logros y recompensas
class Logro(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, help_text="Clase de icono de FontAwesome")
    puntos_honor = models.PositiveIntegerField(default=0)
    puntos_exp = models.PositiveIntegerField(default=0)
    requisito_nivel = models.PositiveIntegerField(default=0)
    es_secreto = models.BooleanField(default=False)
    es_raro = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'
        
    def __str__(self):
        return self.nombre

# Relación entre usuarios y logros
class LogroUsuario(models.Model):
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE, related_name='logros')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtenido = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Logro de Usuario'
        verbose_name_plural = 'Logros de Usuarios'
        unique_together = ('user', 'logro')
        
    def __str__(self):
        return f"{self.user.nickname} - {self.logro.nombre}"
    
class Rango(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, help_text="Clase de icono de FontAwesome")
    puntos_honor = models.PositiveIntegerField(default=0)
    puntos_exp = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Rango'
        verbose_name_plural = 'Rangos'
        
    def __str__(self):
        return self.nombre
class RangoUsuario(models.Model):
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE, related_name='rangos')
    rango = models.ForeignKey(Rango, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Rango de Usuario'
        verbose_name_plural = 'Rangos de Usuarios'
    def __str__(self):
        return f"{self.user.nickname} - {self.rango.nombre}"

# Sistema de eventos y torneos
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    organizador = models.ForeignKey(CreateUser, on_delete=models.SET_NULL, null=True, related_name='eventos_organizados')
    participantes = models.ManyToManyField(CreateUser, related_name='eventos_participados', blank=True)
    premios = models.TextField(blank=True, null=True)
    xp_participacion = models.PositiveIntegerField(default=50)
    honor_ganador = models.PositiveIntegerField(default=100)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        
    def __str__(self):
        return self.nombre
    
    def is_active(self):
        now = timezone.now()
        return self.fecha_inicio <= now <= self.fecha_fin

# Sistema de notificaciones
class Notificacion(models.Model):
    TIPOS = [
        ('LEVEL_UP', 'Subida de Nivel'),
        ('RANK_UP', 'Promoción de Rango'),
        ('ACHIEVEMENT', 'Logro Desbloqueado'),
        ('EVENT', 'Evento Próximo'),
        ('ADMIN', 'Mensaje Administrativo'),
        ('TEAM', 'Mensaje de Equipo'),
    ]
    
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    enlace = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.get_tipo_display()} para {self.user.nickname}"
    
    def mark_as_read(self):
        self.leida = True
        self.save()

# Juegos y estadísticas de juego
class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, help_text="Clase de icono de FontAwesome")
    tiene_rangos = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        
    def __str__(self):
        return self.nombre

# Perfil de juego para cada usuario
class PerfilJuego(models.Model):
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE, related_name='perfiles_juego')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    rango_juego = models.CharField(max_length=50, blank=True, null=True)
    horas_jugadas = models.PositiveIntegerField(default=0)
    personaje_principal = models.CharField(max_length=100, blank=True, null=True)
    nivel_juego = models.PositiveIntegerField(default=1)
    id_jugador = models.CharField(max_length=100, blank=True, null=True, help_text="ID o username dentro del juego")
    es_juego_principal = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Perfil de Juego'
        verbose_name_plural = 'Perfiles de Juego'
        unique_together = ('user', 'juego')
        
    def __str__(self):
        return f"{self.user.nickname} - {self.juego.nombre}"
    
    def save(self, *args, **kwargs):
        # Asegurarse de que solo un juego sea el principal
        if self.es_juego_principal:
            PerfilJuego.objects.filter(user=self.user, es_juego_principal=True).exclude(pk=self.pk).update(es_juego_principal=False)
            
            # Actualizar el juego principal en el perfil del usuario
            self.user.juego_principal = self.juego.nombre
            self.user.save()
            
        super().save(*args, **kwargs)







