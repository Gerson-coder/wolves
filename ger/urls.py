

from django.urls import path
from . import views

urlpatterns = [
    path('gerson2/',views.gerson, name ='gerson'),
]