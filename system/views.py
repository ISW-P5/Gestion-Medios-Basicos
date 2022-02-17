from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse

from .libs.avatar import get_svg_avatar
from .models import BasicMediumExpedient
from .utils import create_default_groups


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
    # Set Permissions and create groups by default system if not exists
    create_default_groups()

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
def responsible_metadata(request):
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
    # Filter basic medium is enable and not have responsibility certificate
    uid = request.GET.get('excluded_id', None)
    try:
        uid = BasicMediumExpedient.objects.get(id=uid)
    except BasicMediumExpedient.DoesNotExist:
        uid = None
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
    return JsonResponse({
        'basic_medium': [
            {
                'value': r.id,
                'label': r.inventory_number + ' - ' + r.name
            } for r in BasicMediumExpedient.objects.filter(is_enable=True)
        ]
    })


@login_required
@permission_required('auth.add_user')
def roles_metadata(request):
    return JsonResponse({
        'groups': [
            {
                'value': r.id,
                'label': r.name
            } for r in Group.objects.all()
        ]
    })


def testing(request):
    # Obtener
    filtrar_usuarios = User.objects.filter(is_staff=True)
    todos_usuarios = User.objects.all()
    # Voy a eliminar Pepe
    try:
        # Editar
        usuario = User.objects.get(username='Pepe')
        usuario.edad = 15
        usuario.save()

        usuario = authenticate(request, {
            'username': 'mackey',
            'password': 'hola'
        })

        # Eliminar
        usuario.delete()
        return "Pepe se elimino"
    except User.DoesNotExist:
        return "Pepe noe existe"

    # Crear
    usuario = User(username='Pepe', first_name='Pepe', last_name='Tono')
    usuario.edad = 15
    usuario.save()

    return HttpResponse(content='<h1>Hola</')