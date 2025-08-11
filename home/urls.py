from django.urls import path

from home import views


urlpatterns = [
    path('gerson/',views.gerson, name ='gerson'),
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
    path('registrar_asistencia/',views.registrar_asistencia, name ='registrar_asistencia'),
    path('verificar-nickname/', views.verificar_nickname, name='verificar_nickname'),
    
    # URLs para gestionar fechas
    path('admin/fechas/', views.admin_fechas, name='admin_fechas'),
    path('admin/fechas/crear/', views.crear_fecha, name='crear_fecha'),
    path('admin/fechas/editar/<int:fecha_id>/', views.editar_fecha, name='editar_fecha'),
    
    # URL para ver logs de depuración
    path('admin/debug-logs/', views.ver_debug_logs, name='ver_debug_logs'),
    path('canciones/', views.canciones, name='canciones'),
]