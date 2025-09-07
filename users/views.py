from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.shortcuts import get_object_or_404
from .forms import UserForm

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count


from .models import CreateUser, Perfil, LogroUsuario, Create_subs

# Configuración de logging
logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def registrar_usuario(request):
    """
    Vista para registro de nuevos usuarios.
    Maneja la creación de cuentas y validación de datos.
    """
    # Si el usuario ya está autenticado, redirigir al perfil
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una sesión activa.")
        return redirect('perfil_usuario')
        
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                # Guardar el usuario con el método personalizado del formulario
                user = form.save()
                
                # Autenticar y hacer login automáticamente
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f"¡Bienvenido al clan Wolves, {user.nickname}! Tu cuenta ha sido creada exitosamente.")
                    logger.info(f"Usuario registrado correctamente: {username}")
                    return redirect('perfil_usuario')
                else:
                    # Este caso es raro pero podría ocurrir
                    messages.warning(request, "Cuenta creada pero no se pudo iniciar sesión automáticamente. Por favor inicia sesión manualmente.")
                    logger.warning(f"Usuario creado pero fallo en autenticación automática: {username}")
                    return redirect('login_usuario')
                    
            except Exception as e:
                logger.error(f"Error en registro de usuario: {str(e)}", exc_info=True)
                messages.error(request, f"Error al crear la cuenta: {str(e)}")
        else:
            # Manejar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            
            logger.warning(f"Intento de registro fallido - Errores de formulario: {form.errors}")
    else:
        form = UserForm()
    
    return render(request, 'registrar_usuario.html', {
        'form': form,
        'titulo': 'Únete al Clan Wolves',
    })

@require_http_methods(["GET", "POST"])
def login_usuario(request):
    """
    Vista para iniciar sesión de usuarios.
    Autentica credenciales y redirige al perfil.
    """
    # Si el usuario ya está autenticado, redirigir al perfil
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una sesión activa.")
        return redirect('perfil_usuario')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Por favor ingresa usuario y contraseña.")
            return render(request, 'login_usuario.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si la cuenta está activa
            if not user.is_active:
                messages.error(request, "Tu cuenta está desactivada. Contacta al administrador.")
                logger.warning(f"Intento de login con cuenta desactivada: {username}")
                return render(request, 'login_usuario.html')
                
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.nickname}!")
            logger.info(f"Login exitoso: {username}")
            return redirect('perfil_usuario')
        else:
            messages.error(request, "Credenciales incorrectas. Verifica tu usuario y contraseña.")
            logger.warning(f"Intento de login fallido para: {username}")
    
    return render(request, 'login_usuario.html', {
        'titulo': 'Iniciar Sesión - Clan Wolves'
    })

@login_required
def perfil_usuario(request):
    usuario = request.user
    perfil = usuario.perfil  # Asumiendo que tienes un modelo de perfil relacionado

    context = {
        'usuario': usuario,
        'perfil': perfil,
        'titulo': f'Perfil de {usuario.nickname}',
        # Otros datos de contexto
    }
    
    return render(request, 'detalle_jugador.html', context)

def logout_usuario(request):
    """
    Vista para cerrar sesión del usuario.
    """
    username = request.user.username if request.user.is_authenticated else "Anónimo"
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    logger.info(f"Logout exitoso: {username}")
    return redirect('login_usuario')

@csrf_exempt  
def editar_perfil(request):
    if request.method == 'POST':
        usuario = request.user
        first_name = request.POST.get('first_name')
        edad = request.POST.get('edad')
        celular = request.POST.get('celular')
        ciudad = request.POST.get('ciudad')
        pais = request.POST.get('pais')

        # Actualizar los campos del usuario
        usuario.first_name = first_name
        usuario.edad = edad
        usuario.celular = celular
        usuario.ciudad = ciudad
        usuario.pais = pais
        usuario.save()

        return JsonResponse({'status': 'success', 'message': 'Perfil actualizado correctamente.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

@login_required
def cambiar_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        usuario = request.user
        usuario.avatar = request.FILES['avatar']
        usuario.save()
        
        return redirect('perfil_usuario')
        
    return JsonResponse({'status': 'error', 'message': 'No se proporcionó una imagen válida.'})

def recuperar_contrasena(request):

    return render(request, 'contraseña_olvidada.html')


def jugadores(request):
   
    # Obtener todos los jugadores con sus perfiles relacionados
    jugadores_list = CreateUser.objects.select_related('perfil').filter(is_active=True)
    
    # Búsqueda por nickname
    search = request.GET.get('search')
    if search:
        jugadores_list = jugadores_list.filter(
            Q(nickname__icontains=search) | 
            Q(username__icontains=search) |
            Q(first_name__icontains=search)
        )
    
    # Filtro por rango
    rango = request.GET.get('rango')
    if rango:
        jugadores_list = jugadores_list.filter(perfil__rango=rango)
    
    # Ordenar por nivel (descendente) y después por puntos de experiencia
    jugadores_list = jugadores_list.order_by('-perfil__nivel', '-perfil__puntos_exp', 'nickname')
    
    # Paginación
    paginator = Paginator(jugadores_list, 12)  # 12 jugadores por página
    page_number = request.GET.get('page')
    jugadores = paginator.get_page(page_number)
    
    # Estadísticas para mostrar
    total_jugadores = CreateUser.objects.filter(is_active=True).count()
    jugadores_online = CreateUser.objects.filter(
        is_active=True, 
        perfil__estado_actividad='ONLINE'
    ).count()
    
    context = {
        'jugadores': jugadores,
        'total_jugadores': total_jugadores,
        'jugadores_online': jugadores_online,
        'search': search,
        'rango_filter': rango,
    }

    return render(request, 'jugadores.html', context)
            
    
def eliminar_jugador(request):
    from .models import CreateUser
    
    jugador_list = CreateUser.objects.all()

    if request.method == 'POST':
        jugador_id = request.POST.get('jugador_id')
        try:
            jugador = CreateUser.objects.get(id=jugador_id)
            jugador_nombre = jugador.nickname or jugador.username
            jugador.delete()
            messages.success(request, f'Jugador {jugador_nombre} eliminado correctamente')
            return redirect('jugadores')
        except CreateUser.DoesNotExist:
            messages.error(request, 'El jugador no existe')
            return redirect('eliminar_jugador')

    return render(request, 'eliminar_jugador.html', {'jugador_list': jugador_list})

def autocomplete_nicknames(request):
    """Endpoint para autocompletado de nicknames"""
    print(f"Autocomplete request received: {request.method}, term: {request.GET.get('term', '')}")
    
    if request.method == 'GET':
        term = request.GET.get('term', '')
        print(f"Searching for term: '{term}', length: {len(term)}")
        
        if len(term) >= 2:  # Solo buscar si hay al menos 2 caracteres
            from .models import CreateUser
            nicknames = CreateUser.objects.filter(
                Q(nickname__icontains=term) | Q(username__icontains=term)
            ).values_list('nickname', 'username', 'id')[:10]  # Limitar a 10 resultados
            
            print(f"Found {nicknames.count() if hasattr(nicknames, 'count') else len(nicknames)} results")
            
            results = []
            for nickname, username, user_id in nicknames:
                display_name = nickname if nickname else username
                results.append({
                    'id': user_id,
                    'label': display_name,
                    'value': display_name,
                    'username': username
                })
            
            print(f"Returning results: {results}")
            return JsonResponse(results, safe=False)
        else:
            return JsonResponse([], safe=False)
    
    return JsonResponse([], safe=False)

