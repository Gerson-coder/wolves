from django.shortcuts import render,redirect



def registrar_usuario(request):
    return render(request,'registrar_usuario.html')





def login_usuario(request):
    return render(request,'login_usuario.html')





