from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse

from .libs.avatar import get_svg_avatar


# Create your views here.
def index(request):
    return redirect('login' if request.user.is_anonymous else 'dashboard')


def admin(request):
    # Render Vue.js Admin Panel
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, "index.html" if request.user.is_staff else "403.html")


def login_api(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)  # Persist login in the system
                return JsonResponse({'status': True})
        return JsonResponse({'status': False})
    return redirect('/login/')


def user_data_api(request):
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username
                        } if not request.user.is_anonymous else {
        'detail': "Las credenciales de autenticación no se proveyeron."
    })


def csrf_api(request):
    return JsonResponse({'detaild': "OK"})


def avatar(request, **kwargs):
    return HttpResponse(get_svg_avatar(request.GET.get('u', 'U'), **request.GET.dict()),
                        content_type='image/svg+xml;base64')


@login_required
def basic_medium_metadata(request):
    return JsonResponse({
        'responsible': [
            {
                'value': r.id,
                'label': r.username
                if r.first_name.strip() == '' or r.last_name.strip() == '' else (r.first_name + ' ' + r.last_name)
            }
            for r in User.objects.filter(is_staff=True)
        ]
    })
