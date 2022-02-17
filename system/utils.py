from django.contrib.auth.models import Permission, Group
from django.db.models import Q


def get_permissions(model, permissions):
    """Obtener permisos apartir de modelo y los diferentes permisos que hay en el sistema"""
    perm_q = Q()
    for perm in permissions:
        perm_q |= Q(codename=perm + '_' + model)
    return Permission.objects.filter(perm_q)


def create_default_groups():
    """Crear los grupos de permisos por defecto (Administrador, Jefe de Departamento, Vicedecano)"""
    if Group.objects.filter(
            Q(name='Administrador') | Q(name='Jefe de Departamento') | Q(name='Vicedecano')).count() < 3:
        # Administrador
        try:
            # Verifico si el group existe
            admin = Group.objects.get(name='Administrador')
        except Group.DoesNotExist:
            # Creo el grupo y le asigno los permisos correspondientes
            admin = Group.objects.create(name='Administrador')
            perm = ['view', 'add', 'change', 'delete']
            admin.permissions.set(get_permissions('user', perm) | get_permissions('group', perm))
            admin.save()

        # Jefe de Departamento
        try:
            # Verifico si el group existe
            jefe = Group.objects.get(name='Jefe de Departamento')
        except Group.DoesNotExist:
            # Creo el grupo y le asigno los permisos correspondientes
            jefe = Group.objects.create(name='Jefe de Departamento')
            perm = ['view', 'add', 'change', 'delete']
            jefe.permissions.set(get_permissions('basicmediumexpedient', ['view']) |
                                 get_permissions('movementticket', perm) | get_permissions('requestticket', perm))
            jefe.save()

        # Vicedecano
        try:
            # Verifico si el group existe
            vicedecano = Group.objects.get(name='Vicedecano')
        except Group.DoesNotExist:
            # Creo el grupo y le asigno los permisos correspondientes
            vicedecano = Group.objects.create(name='Vicedecano')
            perm = ['view', 'add', 'change', 'delete']
            vicedecano.permissions.set(get_permissions('basicmediumexpedient', perm) |
                                       get_permissions('movementticket', perm) |
                                       get_permissions('requestticket', perm) |
                                       get_permissions('responsibilitycertificate', perm))
            vicedecano.save()
