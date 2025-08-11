from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ]
    
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    cargo = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return f"{self.nombre} ({self.dni})"
    
    class Meta:
        verbose_name_plural = "Usuarios"

class SAR(models.Model):
    TIPO_CHOICES = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('red', 'Red'),
        ('otro', 'Otro'),
    ]
    
    URGENCIA_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('validado', 'Validado'),
        ('rechazado', 'Rechazado'),
        ('cerrado', 'Cerrado'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sars')
    codigo = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES, default='media')
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    firma_digital = models.CharField(max_length=255)
    
    def __str__(self):
        return f"SAR-{self.codigo}"
    
    class Meta:
        verbose_name = "SAR"
        verbose_name_plural = "SARs"
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['urgencia']),
        ]

class Documento(models.Model):
    sar = models.ForeignKey(SAR, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    tamano = models.IntegerField(help_text='Tamaño en bytes')
    hash_archivo = models.CharField(max_length=64, help_text='SHA-256')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    ruta_almacenamiento = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Documentos"
        indexes = [
            models.Index(fields=['tipo']),
        ]

class Ticket(models.Model):
    PRIORIDAD_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    COMPLEJIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]
    
    sar = models.OneToOneField(SAR, on_delete=models.CASCADE, related_name='ticket')
    usuario_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')
    codigo = models.CharField(max_length=20, unique=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    complejidad = models.CharField(max_length=10, choices=COMPLEJIDAD_CHOICES)
    horas_estimadas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    
    def __str__(self):
        return f"Ticket-{self.codigo}"
    
    class Meta:
        verbose_name_plural = "Tickets"
        indexes = [
            models.Index(fields=['prioridad']),
            models.Index(fields=['estado']),
        ]

class Solucion(models.Model):
    RESULTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
        ('parcial', 'Parcial'),
    ]
    
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='solucion')
    descripcion = models.TextField()
    fecha_implementacion = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20)
    repositorio = models.CharField(max_length=255, blank=True, null=True)
    resultado_pruebas = models.CharField(max_length=10, choices=RESULTADO_CHOICES)
    
    def __str__(self):
        return f"Solución para {self.ticket}"
    
    class Meta:
        verbose_name = "Solución"
        verbose_name_plural = "Soluciones"

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('email', 'Email'),
        ('push', 'Push'),
        ('sms', 'SMS'),
        ('sistema', 'Sistema'),
    ]
    
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
        ('leido', 'Leído'),
        ('fallido', 'Fallido'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='enviado')
    
    def __str__(self):
        return f"Notificación {self.tipo} para {self.usuario}"
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        indexes = [
            models.Index(fields=['fecha_envio']),
        ]

class SLA(models.Model):
    tipo_servicio = models.CharField(max_length=50)
    tiempo_respuesta = models.IntegerField(help_text='Minutos')
    tiempo_resolucion = models.IntegerField(help_text='Horas')
    metricas = models.TextField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    tickets = models.ManyToManyField(Ticket, through='TicketSLA', related_name='slas')
    
    def __str__(self):
        return f"SLA: {self.tipo_servicio}"
    
    class Meta:
        verbose_name = "SLA"
        verbose_name_plural = "SLAs"

class Auditoria(models.Model):
    RESULTADO_CHOICES = [
        ('aprobado', 'Aprobado'),
        ('observado', 'Observado'),
        ('rechazado', 'Rechazado'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='auditorias')
    accion = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=10, choices=RESULTADO_CHOICES)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Auditoría {self.id} para {self.ticket}"
    
    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        indexes = [
            models.Index(fields=['fecha']),
        ]

class TicketSLA(models.Model):
    CUMPLIMIENTO_CHOICES = [
        ('cumplido', 'Cumplido'),
        ('incumplido', 'Incumplido'),
        ('parcial', 'Parcial'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    cumplimiento = models.CharField(max_length=10, choices=CUMPLIMIENTO_CHOICES, default='cumplido')
    
    def __str__(self):
        return f"Relación Ticket-SLA: {self.ticket} - {self.sla}"
    
    class Meta:
        verbose_name = "Relación Ticket-SLA"
        verbose_name_plural = "Relaciones Ticket-SLA"
        unique_together = ('ticket', 'sla')
