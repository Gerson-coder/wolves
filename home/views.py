from django.shortcuts import render
from users.models import CreateUser

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
def puntos_generales(request):
    return render(request,'puntos_generales.html')

def puntos_torneo(request):
    return render(request,'puntos_torneo.html')


def gallery(request):
    return render(request,'gallery.html')






