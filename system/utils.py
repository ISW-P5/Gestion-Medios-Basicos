from django.contrib.auth.models import Permission, Group
from django.db.models import Q


def get_permissions(model, permissions):
    perm_q = Q()
    for perm in permissions:
        perm_q |= Q(codename=perm + '_' + model)
    return Permission.objects.filter(perm_q)


def create_default_groups():
    """Create default groups in the system"""
    if Group.objects.filter(
            Q(name='Administrador') | Q(name='Jefe de Departamento') | Q(name='Vicedecano')).count() < 3:
        # Administrador
        try:
            admin = Group.objects.get(name='Administrador')
        except Group.DoesNotExist:
            admin = Group.objects.create(name='Administrador')
            perm = ['view', 'add', 'change', 'delete']
            admin.permissions.set(get_permissions('user', perm) | get_permissions('group', perm))
            admin.save()

        # Jefe de Departamento
        try:
            jefe = Group.objects.get(name='Jefe de Departamento')
        except Group.DoesNotExist:
            jefe = Group.objects.create(name='Jefe de Departamento')
            perm = ['view', 'add', 'change', 'delete']
            jefe.permissions.set(get_permissions('basicmediumexpedient', ['view']) |
                                 get_permissions('movementticket', perm) | get_permissions('requestticket', perm))
            jefe.save()

        # Vicedecano
        try:
            vicedecano = Group.objects.get(name='Vicedecano')
        except Group.DoesNotExist:
            vicedecano = Group.objects.create(name='Vicedecano')
            perm = ['view', 'add', 'change', 'delete']
            vicedecano.permissions.set(get_permissions('basicmediumexpedient', perm) |
                                       get_permissions('movementticket', perm) |
                                       get_permissions('requestticket', perm) |
                                       get_permissions('responsibilitycertificate', perm))
            vicedecano.save()
