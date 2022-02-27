import json
from abc import abstractmethod

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets

from .models import BasicMediumExpedient, RequestTicket, MovementTicket, ResponsibilityCertificate
from .serializers import (UserSerializer, BasicMediumExpedientSerializer, RequestTicketSerializer,
                          MovementTicketSerializer, ResponsibilityCertificateSerializer)


class FilterViewSetMixin(viewsets.ModelViewSet):
    """ViewSet para filtrar y ordenar los elementos a devolver en el API"""
    def filter_queryset(self, queryset):
        # Extraer filtro
        filters = self.request.GET.get('filter', None)
        # Extraer orden (ascendente/descendente y la columna)
        try:
            ordering = json.loads(self.request.GET.get('ordering', {'asc': True, 'column': 'id'}))
        except Exception:  # Dont can read ordering data (because is not a json)
            ordering = {'asc': True, 'column': 'id'}
        if filters is not None and filters != '':
            # Extraer filtros de cada ViewSet sino no filtrar elementos
            queryset = self.get_filter(queryset, filters)
        return queryset.order_by(('-' if not ordering.get('asc') else '') + ordering.get('column'))

    @abstractmethod
    def get_filter(self, queryset, value):
        """Filtrar elementos segun el valor especificado"""
        return queryset


class UserViewSet(FilterViewSetMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_filter(self, queryset, value):
        """Filtrar elementos segun: Usuario, Nombre, Apelllido, Email"""
        return queryset.filter(Q(username__contains=value) | Q(first_name__contains=value) |
                               Q(last_name__contains=value) | Q(email__contains=value)).order_by('-date_joined')


class BasicMediumExpedientViewSet(FilterViewSetMixin):
    queryset = BasicMediumExpedient.objects.all()
    serializer_class = BasicMediumExpedientSerializer

    def get_filter(self, queryset, value):
        """Filtrar elementos segun: Nombre, Numero de Inventario, Ubicacion"""
        return queryset.filter(Q(name__contains=value) | Q(inventory_number__contains=value) |
                               Q(location__contains=value) | Q(responsible__username__contains=value) |
                               Q(responsible__first_name__contains=value) | Q(responsible__last_name__contains=value))


class RequestTicketViewSet(FilterViewSetMixin):
    queryset = RequestTicket.objects.all()
    serializer_class = RequestTicketSerializer

    def filter_queryset(self, queryset):
        # Apply filter with special Permissions (Excluding superusers because it have all permissions)
        if self.request.user.has_perm('system.own_requestticket') and not self.request.user.is_superuser:
            queryset = queryset.filter(requester=self.request.user)

        return super(RequestTicketViewSet, self).filter_queryset(queryset)

    def get_filter(self, queryset, value):
        """Filtrar elementos segun: Nombre y Numero de Inventario del Medio basico, Departamento, Solicitante"""
        return queryset.filter(Q(departament__contains=value) | Q(basic_medium__inventory_number__contains=value) |
                               Q(basic_medium__name__contains=value) | Q(requester__username__contains=value))


class MovementTicketViewSet(FilterViewSetMixin):
    queryset = MovementTicket.objects.all()
    serializer_class = MovementTicketSerializer

    def filter_queryset(self, queryset):
        # Apply filter with special Permissions (Excluding superusers because it have all permissions)
        if self.request.user.has_perm('system.own_movementticket') and not self.request.user.is_superuser:
            queryset = queryset.filter(requester=self.request.user)

        return super(MovementTicketViewSet, self).filter_queryset(queryset)

    def get_filter(self, queryset, value):
        """Filtrar elementos segun: Nombre y Numero de Inventario del Medio basico, Lugar nuevo y actual, Solicitante"""
        return queryset.filter(Q(actual_location__contains=value) | Q(new_location__contains=value) |
                               Q(basic_medium__inventory_number__contains=value) |
                               Q(basic_medium__name__contains=value) | Q(requester__username__contains=value))


class ResponsibilityCertificateViewSet(FilterViewSetMixin):
    queryset = ResponsibilityCertificate.objects.filter(basic_medium__is_enable=True)
    serializer_class = ResponsibilityCertificateSerializer

    def get_filter(self, queryset, value):
        """Filtrar elementos segun: Nombre y Numero de Inventario del Medio basico, Carnet, Usuario del responsable"""
        return queryset.filter(Q(identity_card__contains=value) | Q(basic_medium__inventory_number__contains=value) |
                               Q(basic_medium__name__contains=value) | Q(responsible__username__contains=value))
