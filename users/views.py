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
from django.contrib.auth.models import User
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

@csrf_exempt  # Solo para propósitos de desarrollo, considera usar un token CSRF en producción
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

            
    

