from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse

from .libs.avatar import get_svg_avatar


# Create your views here.
# TODO: Create API and JWT with Django Rest API
def index(request):
    return redirect('login' if request.user.is_anonymous else 'dashboard')


def admin(request):
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, "index.html")


def login_api(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(user)  # Persist login in the system
                return JsonResponse({'status': True})
        return JsonResponse({'status': False})
    return redirect('/login/')


def avatar(request, **kwargs):
    return HttpResponse(get_svg_avatar(request.GET.get('u', 'U'), **request.GET.dict()), content_type='image/svg+xml;base64')
