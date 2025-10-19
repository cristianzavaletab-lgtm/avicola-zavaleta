from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def rentabilidad(request):
    return render(request, 'rentabilidad/rentabilidad.html')