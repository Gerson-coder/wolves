from django.urls import path

from home import views


urlpatterns = [
    path('',views.home, name ='index'),
    path('about/',views.about, name ='about'),
    path('torneos/',views.torneos, name ='torneos'),
    path('jugadores/',views.jugadores, name ='jugadores'),
    path('staff/',views.staff, name ='staff'),
    path('eventos/',views.eventos, name ='eventos'),
    path('detalle_evento/',views.detalle_evento, name ='detalle_evento'),
    path('contact/',views.contact, name ='contact'),
    path('gallery/',views.gallery, name ='gallery'),
    
    path('detalle_torneo/',views.detalle_torneo, name ='detalle_torneo'),
    path('puntos_generales/',views.puntos_generales, name ='puntos_generales'),
    path('puntos_torneo/',views.puntos_torneo, name ='puntos_torneo'),
    path('torneos/',views.torneos, name ='torneos'),
]