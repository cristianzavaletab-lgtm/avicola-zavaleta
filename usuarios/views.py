from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def gestion_usuarios(request):
    if request.user.rol != 'dueño':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    return render(request, 'usuarios/gestion.html')