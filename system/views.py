from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse

from .libs.avatar import get_svg_avatar
from .models import BasicMediumExpedient
from .utils import create_default_groups


# Create your views here.
def index(request):
    """Redireccionar a login o al panel administrativo por defecto"""
    return redirect('login' if request.user.is_anonymous else 'dashboard')


def admin(request):
    """Renderizo la pagina principal de Admin hecha en Vue.js"""
    # Render Vue.js Admin Panel
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, "index.html" if request.user.is_staff else "403.html")


def login_api(request):
    """Logear un usuario por medio del API"""
    if request.method == "POST":
        # Al enviar informacion por POST mandarlos a validar en el formulario de autenticacion
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            # Si son validos veo si esta autenticado el usuario
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                # Si se pudo autenticar el usuario entonces lo hago persistente en el sistema
                login(request, user)  # Persist login in the system
                return JsonResponse({'status': True})
        return JsonResponse({'status': False})
    return redirect('/login/')


def user_data_api(request):
    """Devolver datos del usuarios autenticado en el sistema"""
    # Set Permissions and create groups by default system if not exists
    create_default_groups()

    return JsonResponse({
                            'id': request.user.id,
                            'username': request.user.username
                        } if not request.user.is_anonymous else {
        'detail': "Las credenciales de autenticación no se proveyeron."
    })


def csrf_api(request):
    """Generar CSRF Token en las cookies"""
    return JsonResponse({'detaild': "OK"})


def avatar(request, **kwargs):
    """Genera un Avatar como una imagen/svg"""
    return HttpResponse(get_svg_avatar(request.GET.get('u', 'U'), **request.GET.dict()),
                        content_type='image/svg+xml;base64')


@login_required
def responsible_metadata(request):
    """Obtener todos los responsables con su nombre de usuario o nombre completo"""
    # Extraemos un parametro all para devolver todos o solo los administradores
    get_all = request.GET.get('all', None)
    if get_all == 'false':
        get_all = None
    return JsonResponse({
        'responsible': [
            {
                'value': r.id,
                'label': r.username
                if r.first_name.strip() == '' or r.last_name.strip() == '' else (r.first_name + ' ' + r.last_name)
            }
            for r in (User.objects.filter(is_staff=True) if get_all is None else User.objects.all())
        ]
    })


@login_required
def basic_medium_without_certificate_metadata(request):
    """Obtener Medios Basicos que esten habilitados y que no tengan un acta de responsabilidad"""
    # Extraigo el uid (Para incluir el ID del propio medio asignado)
    uid = request.GET.get('included_id', None)
    try:
        uid = BasicMediumExpedient.objects.get(id=uid)
    except BasicMediumExpedient.DoesNotExist:
        uid = None
    # Extraigo todos los Medios Basicos que no tengan un acta de responsabilidad y agrego el incluido
    return JsonResponse({
        'basic_medium': [
            {
                'value': r.id,
                'label': r.inventory_number + ' - ' + r.name
            } for r in BasicMediumExpedient.objects.filter(is_enable=True, responsibilitycertificate__isnull=True)
        ] + ([
             {
                 'value': uid.id,
                 'label': uid.inventory_number + ' - ' + uid.name
             }
             ] if uid is not None else [])
    })


@login_required
def basic_medium_metadata(request):
    """Obtener Medios Basicos"""
    return JsonResponse({
        'basic_medium': [
            {
                'value': r.id,
                'label': r.inventory_number + ' - ' + r.name
            } for r in BasicMediumExpedient.objects.filter(is_enable=True)
        ]
    })


@login_required
def roles_metadata(request):
    """Obtener Roles"""
    return JsonResponse({
        'groups': [
            {
                'value': r.id,
                'label': r.name
            } for r in Group.objects.all()
        ]
    })
