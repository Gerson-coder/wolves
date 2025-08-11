from django.shortcuts import render, get_object_or_404
from users.models import CreateUser
from home.models import Asistencia, Fecha
from home.forms import AsistenciaForm, FechaForm
from django.shortcuts import redirect
from django.db.models import Count, Max
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
from datetime import datetime

# Configurar el logger para depuración
logger = logging.getLogger('asistencia_debug')


def gerson(request):
    return render(request,'gerson.html')

# Create your views here.
def home(request):

     # Obtener todos los usuarios activos (puedes ajustar el filtro según necesites)
    usuarios = CreateUser.objects.filter(is_active=True)
    
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def torneos(request):
    return render(request,'torneos.html')

def contact(request):
    return render(request,'contact.html')
def faq(request):
    return render(request,'faq.html')

def jugadores(request):
    return render(request,'jugadores.html')
def staff(request):
    return render(request,'staff.html')

def eventos(request):
    return render(request,'eventos.html')

def detalle_evento(request):
    return render(request,'detalle_evento.html')


def detalle_torneo(request):
    return render(request,'detalle_torneo.html')


def actualizar_grupos():
    """
    Función auxiliar para actualizar los grupos de todos los usuarios.
    Esta función ahora delega al método del modelo.
    """
    return Asistencia.actualizar_grupos()


def verificar_nickname(request):
    """
    Verifica si un nickname existe y retorna la información del usuario
    """
    if request.method == "GET" and 'nickname' in request.GET:
        nickname = request.GET['nickname']
        try:
            # Buscar el último registro del usuario con ese nickname
            usuario = Asistencia.objects.filter(nickname=nickname).order_by('-fecha').first()
            if usuario:
                # Obtener el total de registros para este nickname
                total_registros = Asistencia.objects.filter(nickname=nickname).count()
                
                # Obtener la fecha actual para verificar si ya hay registro hoy
                from datetime import date
                hoy = date.today()
                registro_hoy = Asistencia.objects.filter(nickname=nickname, fecha=hoy).exists()
                
                # Si el usuario existe, retornar sus datos
                return JsonResponse({
                    'existe': True,
                    'apodo': usuario.apodo,
                    'grupo': usuario.grupo,
                    'puntos_dia': usuario.puntos,
                    'puntos_acumulados': usuario.puntos_acumulados,
                    'total_registros': total_registros,
                    'registro_hoy': registro_hoy,
                    'avatar_url': usuario.avatar.url if usuario.avatar else None
                })
        except Exception as e:
            print(f"Error verificando nickname: {e}")
        
    # Si no existe o hay error, retornar que no existe
    return JsonResponse({'existe': False})


def puntos_generales(request):
    # Actualizar grupos antes de mostrar la página
    actualizar_grupos()
    
    # Obtener todas las fechas para el selector
    todas_fechas = Fecha.objects.filter(activa=True).order_by('-fecha')
    
    # Obtener parámetros de fecha del request
    fecha_id = request.GET.get('fecha_id')
    fecha_personalizada = request.GET.get('fecha')
    fecha_seleccionada = None
      
    # Filtrar asistencias según los parámetros recibidos
    if fecha_id:
        # Si se proporciona un ID de fecha específico
        try:
            fecha_seleccionada = Fecha.objects.get(id=fecha_id)
            # Obtener asistencias para esa fecha
            asistencias_lista = list(Asistencia.objects.filter(fecha=fecha_seleccionada.fecha))
            
            # Agrupar por puntos acumulados
            asistencias_por_puntos = {}
            for asistencia in asistencias_lista:
                puntos = asistencia.puntos_acumulados
                if puntos not in asistencias_por_puntos:
                    asistencias_por_puntos[puntos] = []
                asistencias_por_puntos[puntos].append(asistencia)
            
            # Para cada grupo de puntos, ordenar por hora de registro
            for puntos, grupo in asistencias_por_puntos.items():
                grupo.sort(key=lambda x: x.fecha)  # Ordenar por hora de registro ascendente
            
            # Crear lista final ordenada
            asistencias = []
            for puntos in sorted(asistencias_por_puntos.keys(), reverse=True):
                asistencias.extend(asistencias_por_puntos[puntos])
            
        except Fecha.DoesNotExist:
            asistencias = []
    elif fecha_personalizada:
        # Si se proporciona una fecha personalizada
        from datetime import datetime
        try:
            # Convertir la fecha de string a objeto date
            fecha_dt = datetime.strptime(fecha_personalizada, '%Y-%m-%d').date()
            
            # Buscar si existe un evento en esta fecha
            fecha_evento = Fecha.objects.filter(fecha=fecha_dt).first()
            
            if fecha_evento:
                fecha_seleccionada = fecha_evento
                # Obtener asistencias para esa fecha
                asistencias_lista = list(Asistencia.objects.filter(fecha=fecha_dt))
            else:
                # Si no hay evento en esa fecha, buscar por la fecha de asistencia
                asistencias_lista = list(Asistencia.objects.filter(fecha=fecha_dt))
                # Crear un objeto temporal para mostrar la fecha seleccionada en la plantilla
                from types import SimpleNamespace
                fecha_seleccionada = SimpleNamespace(nombre=f"Asistencias del día", fecha=fecha_dt)
            
            # Agrupar por puntos acumulados
            asistencias_por_puntos = {}
            for asistencia in asistencias_lista:
                puntos = asistencia.puntos_acumulados
                if puntos not in asistencias_por_puntos:
                    asistencias_por_puntos[puntos] = []
                asistencias_por_puntos[puntos].append(asistencia)
            
            # Para cada grupo de puntos, ordenar por hora de registro
            for puntos, grupo in asistencias_por_puntos.items():
                grupo.sort(key=lambda x: x.fecha)  # Ordenar por hora de registro ascendente
            
            # Crear lista final ordenada
            asistencias = []
            for puntos in sorted(asistencias_por_puntos.keys(), reverse=True):
                asistencias.extend(asistencias_por_puntos[puntos])
            
        except (ValueError, TypeError):
            # Error al convertir la fecha
            asistencias = []
    else:
        # Si no hay filtro de fecha, mostrar el último registro de cada jugador
        nicknames = Asistencia.objects.values_list('nickname', flat=True).distinct()
        
        # Obtener la fecha del evento más reciente
        ultima_fecha_evento = Fecha.objects.filter(activa=True).order_by('-fecha').first()
        
        if ultima_fecha_evento:
            # Obtener los registros de la última fecha activa
            asistencias_ultima_fecha = list(Asistencia.objects.filter(
                fecha=ultima_fecha_evento.fecha
            ).order_by('fecha'))  # Orden ascendente por hora de registro
            
            # Crear un diccionario para mapear nicknames a su hora de registro en la última fecha
            hora_registro_por_nickname = {a.nickname: a.fecha for a in asistencias_ultima_fecha}
            
            # Obtener el último registro de cada jugador
            asistencias = []
            for nickname in nicknames:
                ultimo_registro = Asistencia.objects.filter(nickname=nickname).order_by('-fecha').first()
                if ultimo_registro:
                    asistencias.append(ultimo_registro)
            
            # Agrupar jugadores por puntos acumulados
            jugadores_por_puntos = {}
            for asistencia in asistencias:
                puntos = asistencia.puntos_acumulados
                if puntos not in jugadores_por_puntos:
                    jugadores_por_puntos[puntos] = []
                jugadores_por_puntos[puntos].append(asistencia)
            
            # Para cada grupo de jugadores con mismos puntos, ordenarlos por hora de registro
            from datetime import datetime
            for puntos, grupo_asistencias in jugadores_por_puntos.items():
                grupo_asistencias.sort(key=lambda x: hora_registro_por_nickname.get(x.nickname, datetime.max))
            
            # Crear la lista final ordenada: primero por puntos (descendente) y luego por hora de registro
            asistencias = []
            for puntos in sorted(jugadores_por_puntos.keys(), reverse=True):
                asistencias.extend(jugadores_por_puntos[puntos])
        else:
            # Si no hay fechas activas, ordenar solo por puntos
            asistencias = []
            for nickname in nicknames:
                ultimo_registro = Asistencia.objects.filter(nickname=nickname).order_by('-fecha').first()
                if ultimo_registro:
                    asistencias.append(ultimo_registro)
            
            # Ordenar por puntos acumulados y puntos del día
            asistencias.sort(key=lambda x: (-x.puntos_acumulados, -x.puntos))
    
    # Agrupar asistencias por grupo
    asistencias_por_grupo = {}
    for asistencia in asistencias:
        grupo = asistencia.grupo
        if grupo not in asistencias_por_grupo:
            asistencias_por_grupo[grupo] = []
        asistencias_por_grupo[grupo].append(asistencia)
    
    # Ordenar los grupos alfabéticamente (A, B, C)
    grupos_ordenados = sorted(asistencias_por_grupo.keys())
    
    context = {
        'asistencias': asistencias,
        'asistencias_por_grupo': asistencias_por_grupo,
        'grupos_ordenados': grupos_ordenados,
        'todas_fechas': todas_fechas,
        'fecha_seleccionada': fecha_seleccionada,
        'fecha_personalizada': fecha_personalizada,
    }
    return render(request, 'puntos_generales.html', context)



def registrar_asistencia(request):
    """
    Vista para registrar una nueva asistencia o actualizar una existente.
    Utiliza los métodos del modelo para la lógica de negocio.
    """
    inicio = datetime.now()
    logger.debug(f"[INICIO] Vista registrar_asistencia - Método: {request.method}, Timestamp: {inicio.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    
    # Obtener todas las fechas activas para el formulario
    fechas_activas = Fecha.objects.filter(activa=True).order_by('-fecha')
    logger.debug(f"Fechas activas encontradas: {fechas_activas.count()}")
    
    if request.method == 'POST':
        logger.debug(f"Procesando formulario POST - Datos: {request.POST}")
        form = AsistenciaForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Formulario válido, preparando datos para registro/actualización")
            # Preparar los datos para el registro/actualización
            datos = {
                'nickname': form.cleaned_data['nickname'],
                'apodo': form.cleaned_data['apodo'],
                'puntos': form.cleaned_data['puntos'],
                'fecha': form.cleaned_data['fecha'],
                'avatar': form.cleaned_data['avatar'],
            }
            
            logger.debug(f"Datos preparados: Nickname: {datos['nickname']}, Puntos: {datos['puntos']}, Fecha: {datos['fecha']}")
            
            # Usar el método del modelo para registrar o actualizar
            asistencia = Asistencia.registrar_o_actualizar(datos)
            
            logger.debug(f"Asistencia registrada/actualizada con ID: {asistencia.id}")
            
            # Actualizar los grupos de todos los jugadores
            logger.debug("Iniciando actualización de grupos")
            jugadores_actualizados = actualizar_grupos()
            logger.debug(f"Grupos actualizados para {jugadores_actualizados} jugadores")
            
            fin = datetime.now()
            duracion = (fin - inicio).total_seconds()
            logger.debug(f"[FIN] Vista registrar_asistencia - Redirigiendo a puntos_generales, Duración total: {duracion} segundos")
            
            return redirect('puntos_generales')
        else:
            logger.error(f"Formulario inválido. Errores: {form.errors}")
            print(form.errors)  # Imprime los errores para depuración
    else:
        logger.debug("Método GET, mostrando formulario vacío")
        form = AsistenciaForm()
    
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    logger.debug(f"[FIN] Vista registrar_asistencia - Renderizando formulario, Duración total: {duracion} segundos")
    
    return render(request, 'registrar_asistencia.html', {'form': form, 'fechas_activas': fechas_activas})

def puntos_torneo(request):
    return render(request,'puntos_torneo.html')


def gallery(request):
    return render(request,'gallery.html')

# Función para verificar si un usuario es staff
def es_staff(user):
    return user.is_staff

@login_required
@user_passes_test(es_staff)
def admin_fechas(request):
    """Vista para administrar las fechas de eventos"""
    fechas = Fecha.objects.all().order_by('-fecha')
    
    context = {
        'fechas': fechas,
    }
    return render(request, 'admin_fechas.html', context)

@login_required
@user_passes_test(es_staff)
def crear_fecha(request):
    """Vista para crear una nueva fecha de evento"""
    if request.method == 'POST':
        form = FechaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_fechas')
    else:
        form = FechaForm()
    
    context = {
        'form': form,
        'accion': 'Crear',
    }
    return render(request, 'form_fecha.html', context)

@login_required
@user_passes_test(es_staff)
def editar_fecha(request, fecha_id):
    """Vista para editar una fecha existente"""
    fecha = get_object_or_404(Fecha, id=fecha_id)
    
    if request.method == 'POST':
        form = FechaForm(request.POST, instance=fecha)
        if form.is_valid():
            form.save()
            return redirect('admin_fechas')
    else:
        form = FechaForm(instance=fecha)
    
    context = {
        'form': form,
        'fecha': fecha,
        'accion': 'Editar',
    }
    return render(request, 'form_fecha.html', context)

@login_required
@user_passes_test(es_staff)
def ver_debug_logs(request):
    """Vista para ver los logs de depuración de asistencias"""
    try:
        import os
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        log_file = os.path.join(log_dir, 'asistencia_debug.log')
        
        # Verificar si el archivo existe
        if not os.path.exists(log_file):
            return render(request, 'error.html', {'error': 'El archivo de logs no existe'})
        
        # Leer las últimas 500 líneas del archivo (para no sobrecargar la página)
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            log_entries = lines[-500:]  # Últimas 500 líneas
        
        # Procesar las entradas para mostrarlas mejor
        formatted_entries = []
        for entry in log_entries:
            parts = entry.strip().split(' - ', 2)
            if len(parts) >= 3:
                timestamp = parts[0]
                level = parts[1]
                message = parts[2]
                
                formatted_entries.append({
                    'timestamp': timestamp,
                    'level': level,
                    'message': message,
                    'is_start': '[INICIO]' in message,
                    'is_end': '[FIN]' in message,
                    'is_error': level == 'ERROR'
                })
        
        context = {
            'log_entries': formatted_entries,
            'total_entries': len(formatted_entries),
            'log_file': log_file
        }
        return render(request, 'debug_logs.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': f'Error al leer logs: {str(e)}'})


def canciones(request):
    from home.models import Cancion
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        genero = request.POST.get('genero')
        duracion = request.POST.get('duracion')
        artista = request.POST.get('artista')
        puntuacion = request.POST.get('puntuacion')
        
        # Crear nueva canción
        cancion = Cancion(
            nombre=nombre,
            genero=genero,
            duracion=duracion,
            artista=artista,
            puntuacion=puntuacion
        )
        cancion.save()
        
        # Redireccionar para evitar reenvío del formulario
        from django.shortcuts import redirect
        return redirect('canciones')
    
    # Obtener todas las canciones para mostrarlas
    canciones = Cancion.objects.all().order_by('-id')
    
    return render(request, 'canciones.html', {'canciones': canciones})




