from django.contrib import admin
from .models import Asistencia, Fecha

class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'apodo', 'puntos', 'puntos_acumulados', 'grupo', 'fecha',)
    list_filter = ('grupo', 'fecha',)
    search_fields = ('nickname', 'apodo')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-puntos_acumulados')

class FechaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'activa', 'total_asistencias')
    list_filter = ('activa', 'fecha')
    search_fields = ('nombre',)
    ordering = ('-fecha',)
    
    def total_asistencias(self, obj):
        return obj.asistencias.count()
    total_asistencias.short_description = 'Total de asistencias'

admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Fecha, FechaAdmin)