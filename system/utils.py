from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


def get_permissions(model, permissions):
    """Obtener permisos apartir de modelo y los diferentes permisos que hay en el sistema"""
    perm_q = Q()
    for perm in permissions:
        perm_q |= Q(codename=perm + '_' + model)
    return Permission.objects.filter(perm_q)


def create_special_permissions():
    """Crear los permisos por defecto en el sistema (Permisos extra para los Vales de Solicitud y Movimiento)"""
    # Getting Content Type
    request_ticket_content_type = ContentType.objects.get(app_label='system', model='requestticket')
    movement_ticket_content_type = ContentType.objects.get(app_label='system', model='movementticket')

    # Creating permissions
    own_request_ticket, _ = Permission.objects.get_or_create(codename='own_requestticket',
                                                             name='Can only view own Vale de Solicitud',
                                                             content_type=request_ticket_content_type)
    own_movement_ticket, _ = Permission.objects.get_or_create(codename='own_movementticket',
                                                              name='Can only view own Vale de Movimiento',
                                                              content_type=movement_ticket_content_type)
    return own_request_ticket, own_movement_ticket


def create_default_groups():
    """Crear los grupos de permisos por defecto (Administrador, Jefe de Departamento, Vicedecano)"""
    if Group.objects.filter(
            Q(name='Administrador') | Q(name='Jefe de Departamento') | Q(name='Vicedecano')).count() < 3:
        # Creo el grupo y le asigno los permisos correspondientes
        # Administrador
        admin, created = Group.objects.get_or_create(name='Administrador')
        if created:
            perm = ['view', 'add', 'change', 'delete']
            admin.permissions.set(get_permissions('user', perm) | get_permissions('group', perm))
            admin.save()

        # Jefe de Departamento
        jefe, created = Group.objects.get_or_create(name='Jefe de Departamento')
        if created:
            # Extract special permissions
            own_request_ticket, own_movement_ticket = create_special_permissions()

            perm = ['view', 'add', 'change', 'delete', 'own']
            jefe.permissions.set(get_permissions('basicmediumexpedient', ['view']) |
                                 get_permissions('movementticket', perm) | get_permissions('requestticket', perm))
            jefe.permissions.add(own_request_ticket)
            jefe.permissions.add(own_movement_ticket)
            jefe.save()

        # Vicedecano
        vicedecano, created = Group.objects.get_or_create(name='Vicedecano')
        if created:
            perm = ['view', 'add', 'change', 'delete']
            vicedecano.permissions.set(get_permissions('basicmediumexpedient', perm) |
                                       get_permissions('movementticket', perm) |
                                       get_permissions('requestticket', perm) |
                                       get_permissions('responsibilitycertificate', perm))
            vicedecano.save()
