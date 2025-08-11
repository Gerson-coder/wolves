from django.db import models
import os
import logging
from datetime import datetime

# Configurar el logger para depuración
logger = logging.getLogger('asistencia_debug')
logger.setLevel(logging.DEBUG)

# Crear un manejador de archivo para guardar los logs
import os
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'asistencia_debug.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Definir el formato del log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(file_handler)

# Create your models here.


CHOICES_GRUPO = [
    ('A','A'),
    ('B','B'),
    ('C','C'),
]


class Fecha(models.Model):
    """
    Modelo para registrar las fechas de eventos/asistencias
    """
    nombre = models.CharField(max_length=100, help_text="Nombre descriptivo del día (ej: 'Día 1 - Torneo Wolves')")
    fecha = models.DateField(unique=True, help_text="Fecha del evento")
    activa = models.BooleanField(default=True, help_text="Indica si esta fecha está activa para registrar asistencias")
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Fecha'
        verbose_name_plural = 'Fechas'
    
    def __str__(self):
        return f"{self.nombre} ({self.fecha.strftime('%d/%m/%Y')})"


class Asistencia(models.Model):
    nickname = models.CharField(max_length=255)
    apodo = models.CharField(max_length=255, blank=True, null=True, default='')
    puntos = models.IntegerField()
    puntos_acumulados = models.IntegerField(default=0)
    grupo = models.CharField(max_length=255, choices=CHOICES_GRUPO)
    fecha = models.DateTimeField(auto_now_add=False, help_text="Fecha y hora de registro")
    # Relación con el modelo Fecha (opcional)
   
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.nickname
    
    @classmethod
    def registrar_o_actualizar(cls, datos):
        """
        Registra una nueva asistencia o actualiza una existente si ya existe para el mismo nickname y fecha.
        
        Args:
            datos: Un diccionario con los datos de la asistencia (nickname, fecha, puntos, etc.)
            
        Returns:
            La instancia de Asistencia creada o actualizada
        """
        inicio = datetime.now()
        nickname = datos.get('nickname')
        fecha = datos.get('fecha')
        
        logger.debug(f"[INICIO] Registrar o actualizar asistencia - Nickname: {nickname}, Fecha: {fecha}, Timestamp: {inicio.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.debug(f"Datos recibidos: {datos}")
        
        # Verificar si ya existe un registro para este nickname en la misma fecha
        registro_existente = cls.objects.filter(nickname=nickname, fecha=fecha).first()
        
        resultado = None
        if registro_existente:
            logger.debug(f"Encontrado registro existente para {nickname} en fecha {fecha}")
            resultado = cls.actualizar_registro_existente(registro_existente, datos)
        else:
            logger.debug(f"No se encontró registro existente para {nickname} en fecha {fecha}. Creando nuevo registro.")
            resultado = cls.crear_nuevo_registro(datos)
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        logger.debug(f"[FIN] Registrar o actualizar asistencia - Nickname: {nickname}, Duración: {duracion} segundos")
        
        return resultado
    
    @classmethod
    def actualizar_registro_existente(cls, registro, datos):
        """
        Actualiza un registro de asistencia existente
        
        Args:
            registro: La instancia de Asistencia a actualizar
            datos: Un diccionario con los nuevos datos
            
        Returns:
            La instancia de Asistencia actualizada
        """
        inicio = datetime.now()
        logger.debug(f"[INICIO] Actualizar registro existente - Nickname: {registro.nickname}, ID: {registro.id}, Timestamp: {inicio.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        logger.debug(f"Datos antes de actualizar: Puntos: {registro.puntos}, Puntos acumulados: {registro.puntos_acumulados}, Grupo: {registro.grupo}")
        
        # Sumar los nuevos puntos a los puntos del día existentes
        puntos_nuevos = datos.get('puntos', 0)
        puntos_actuales = registro.puntos
        
        # Actualizar puntos del día (sumando los nuevos)
        registro.puntos = puntos_actuales + puntos_nuevos
        
        # Actualizar puntos acumulados (sumando solo los nuevos puntos)
        registro.puntos_acumulados = registro.puntos_acumulados + puntos_nuevos
        
        # Actualizar avatar si se proporciona uno nuevo
        if 'avatar' in datos and datos['avatar']:
            # Si había un avatar anterior, eliminarlo para no acumular archivos
            if registro.avatar:
                try:
                    # Intentar eliminar el archivo físico
                    if os.path.isfile(registro.avatar.path):
                        os.remove(registro.avatar.path)
                except Exception as e:
                    logger.error(f"Error al eliminar avatar anterior: {e}")
            registro.avatar = datos['avatar']
        
        # Actualizar apodo si se proporciona
        if 'apodo' in datos and datos['apodo']:
            registro.apodo = datos['apodo']
        
        # Guardar cambios
        registro.save()
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        logger.debug(f"Datos después de actualizar: Puntos: {registro.puntos}, Puntos acumulados: {registro.puntos_acumulados}, Grupo: {registro.grupo}")
        logger.debug(f"[FIN] Actualizar registro existente - Nickname: {registro.nickname}, ID: {registro.id}, Duración: {duracion} segundos")
        
        return registro
    
    @classmethod
    def crear_nuevo_registro(cls, datos):
        """
        Crea un nuevo registro de asistencia
        
        Args:
            datos: Un diccionario con los datos de la asistencia
            
        Returns:
            La nueva instancia de Asistencia
        """
        inicio = datetime.now()
        nickname = datos.get('nickname')
        logger.debug(f"[INICIO] Crear nuevo registro - Nickname: {nickname}, Timestamp: {inicio.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        
        # Buscar registros previos del mismo jugador
        registros_previos = cls.objects.filter(nickname=nickname).order_by('-fecha')
        
        # Crear nueva instancia
        nueva_asistencia = cls(
            nickname=nickname,
            apodo=datos.get('apodo', ''),
            puntos=datos.get('puntos', 0),
            fecha=datos.get('fecha')
        )
        
        # Si hay avatar, asignarlo
        if 'avatar' in datos and datos['avatar']:
            nueva_asistencia.avatar = datos['avatar']
        
        # Calcular puntos acumulados y asignar grupo
        if registros_previos.exists():
            # Si hay registros previos, obtener el último
            ultimo_registro = registros_previos.first()
            logger.debug(f"Encontrado registro previo para {nickname}. Último registro ID: {ultimo_registro.id}, Fecha: {ultimo_registro.fecha}")
            
            # Sumar puntos al acumulado anterior
            nueva_asistencia.puntos_acumulados = ultimo_registro.puntos_acumulados + nueva_asistencia.puntos
            
            # Usar el mismo grupo temporalmente (se actualizará después)
            nueva_asistencia.grupo = ultimo_registro.grupo
            
            # Conservar el avatar existente si no se sube uno nuevo
            if not nueva_asistencia.avatar and ultimo_registro.avatar:
                nueva_asistencia.avatar = ultimo_registro.avatar
                
            # Asegurarse de mantener el mismo apodo si no se proporciona uno nuevo
            if not nueva_asistencia.apodo and ultimo_registro.apodo:
                nueva_asistencia.apodo = ultimo_registro.apodo
                
            logger.debug(f"Datos del último registro: Puntos: {ultimo_registro.puntos}, Puntos acumulados: {ultimo_registro.puntos_acumulados}, Grupo: {ultimo_registro.grupo}")
        else:
            # Si es el primer registro, los puntos acumulados son iguales a los puntos del día
            nueva_asistencia.puntos_acumulados = nueva_asistencia.puntos
            # Asignar grupo C por defecto para nuevos jugadores
            nueva_asistencia.grupo = 'C'
            logger.debug(f"No se encontraron registros previos para {nickname}. Primer registro.")
        
        # Guardar el nuevo registro
        nueva_asistencia.save()
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        logger.debug(f"Nuevo registro creado - ID: {nueva_asistencia.id}, Puntos: {nueva_asistencia.puntos}, Puntos acumulados: {nueva_asistencia.puntos_acumulados}, Grupo: {nueva_asistencia.grupo}")
        logger.debug(f"[FIN] Crear nuevo registro - Nickname: {nickname}, Duración: {duracion} segundos")
        
        return nueva_asistencia
    
    @classmethod
    def actualizar_grupos(cls):
        """
        Actualiza los grupos de todos los usuarios basado en su posición en el ranking de puntos acumulados:
        - Grupo A: Top 10
        - Grupo B: Posiciones 11-25
        - Grupo C: Posición 26 en adelante
        
        Dentro del mismo grupo y con mismos puntos, se prioriza el orden de llegada (registro).
        
        Returns:
            int: Número de jugadores únicos actualizados
        """
        inicio = datetime.now()
        logger.debug(f"[INICIO] Actualizar grupos - Timestamp: {inicio.strftime('%Y-%m-%d %H:%M:%S.%f')}")
        
        from django.db.models import Max, Min
        
        # Obtener la fecha del evento más reciente
        ultima_fecha = cls.objects.aggregate(Max('fecha'))['fecha__max']
        logger.debug(f"Fecha más reciente encontrada: {ultima_fecha}")
        
        # Obtener jugadores únicos con sus puntos acumulados máximos (último registro)
        jugadores_unicos = cls.objects.values('nickname').annotate(
            max_puntos=Max('puntos_acumulados')
        )
        logger.debug(f"Total de jugadores únicos encontrados: {len(jugadores_unicos)}")
        
        # Para cada jugador, obtener su último registro por fecha
        jugadores_info = []
        for jugador in jugadores_unicos:
            nickname = jugador['nickname']
            max_puntos = jugador['max_puntos']
            
            # Obtener el último registro del jugador
            ultimo_registro = cls.objects.filter(nickname=nickname).order_by('-fecha').first()
            
            # Si hay un registro para la última fecha, obtener la hora de registro
            registro_fecha_actual = cls.objects.filter(
                nickname=nickname, 
                fecha__date=ultima_fecha.date() if ultima_fecha else None
            ).order_by('fecha').first()
            
            # Hora de registro para la última fecha (si existe)
            hora_registro = registro_fecha_actual.fecha if registro_fecha_actual else None
            
            jugadores_info.append({
                'nickname': nickname,
                'puntos': max_puntos,
                'hora_registro': hora_registro,
                'ultimo_registro': ultimo_registro
            })
            
            logger.debug(f"Jugador: {nickname}, Puntos: {max_puntos}, Hora registro: {hora_registro}")
        
        # Crear un diccionario para agrupar jugadores por puntos
        jugadores_por_puntos = {}
        for jugador in jugadores_info:
            puntos = jugador['puntos']
            if puntos not in jugadores_por_puntos:
                jugadores_por_puntos[puntos] = []
            jugadores_por_puntos[puntos].append(jugador)
        
        # Para cada grupo de jugadores con mismos puntos, ordenarlos por hora de registro
        for puntos, grupo_jugadores in jugadores_por_puntos.items():
            logger.debug(f"Ordenando grupo de jugadores con {puntos} puntos. Total jugadores: {len(grupo_jugadores)}")
            grupo_jugadores.sort(key=lambda x: x['hora_registro'] or ultima_fecha)
            
            # Registrar el orden después de ordenar
            logger.debug(f"Orden después de ordenar jugadores con {puntos} puntos:")
            for idx, jugador in enumerate(grupo_jugadores):
                logger.debug(f"  {idx+1}. {jugador['nickname']} - Hora registro: {jugador['hora_registro']}")
        
        # Crear la lista final ordenada: primero por puntos (descendente) y luego por hora de registro
        jugadores_ordenados = []
        for puntos in sorted(jugadores_por_puntos.keys(), reverse=True):
            jugadores_ordenados.extend(jugadores_por_puntos[puntos])
        
        # Registrar el orden final
        logger.debug("Orden final de jugadores:")
        for idx, jugador in enumerate(jugadores_ordenados):
            logger.debug(f"{idx+1}. {jugador['nickname']} - Puntos: {jugador['puntos']}, Hora registro: {jugador['hora_registro']}")
        
        # Actualizar el grupo de cada jugador según su posición
        actualizados = 0
        for idx, jugador in enumerate(jugadores_ordenados, 1):  # empezamos en 1 para contar desde la posición 1
            ultimo_registro = jugador['ultimo_registro']
            
            # Determinar el grupo según la posición
            if idx <= 10:
                grupo = 'A'
            elif idx <= 25:
                grupo = 'B'
            else:
                grupo = 'C'
            
            # Actualizar el grupo si es necesario
            if ultimo_registro and ultimo_registro.grupo != grupo:
                grupo_anterior = ultimo_registro.grupo
                ultimo_registro.grupo = grupo
                ultimo_registro.save()
                actualizados += 1
                logger.debug(f"Actualizado grupo de {jugador['nickname']}: {grupo_anterior} -> {grupo} (Posición: {idx})")
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        logger.debug(f"[FIN] Actualizar grupos - Jugadores actualizados: {actualizados}, Duración: {duracion} segundos")
        
        return len(jugadores_ordenados)






class Cancion(models.Model):
    nombre = models.CharField(max_length=255)
    genero = models.CharField(max_length=255)
    duracion = models.CharField(max_length=255)
    artista = models.CharField(max_length=255)
    puntuacion = models.IntegerField()

    def __str__(self):
        return self.nombre






