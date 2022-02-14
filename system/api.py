import json

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets

from .models import BasicMediumExpedient, RequestTicket, MovementTicket, ResponsibilityCertificate
from .serializers import (UserSerializer, BasicMediumExpedientSerializer, RequestTicketSerializer,
                          MovementTicketSerializer, ResponsibilityCertificateSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer

    def filter_queryset(self, queryset):
        filters = self.request.GET.get('filter', None)
        if filters is not None and filters != '':
            return queryset.filter(Q(username__contains=filters) | Q(first_name__contains=filters) |
                                   Q(last_name__contains=filters)).order_by('-date_joined')
        return queryset


class BasicMediumExpedientViewSet(viewsets.ModelViewSet):
    queryset = BasicMediumExpedient.objects.filter(is_enable=True)
    serializer_class = BasicMediumExpedientSerializer

    def filter_queryset(self, queryset):
        filters = self.request.GET.get('filter', None)
        try:
            ordering = json.loads(self.request.GET.get('ordering', {'asc': True, 'column': 'id'}))
        except Exception:  # Dont can read ordering data (because is not a json)
            ordering = {'asc': True, 'column': 'id'}
        if filters is not None and filters != '':
            return queryset.filter(Q(name__contains=filters) |
                                   Q(inventory_number__contains=filters) |
                                   Q(location__contains=filters))
        return queryset.order_by(('-' if not ordering.get('asc') else '') + ordering.get('column'))


class RequestTicketViewSet(viewsets.ModelViewSet):
    queryset = RequestTicket.objects.all()
    serializer_class = RequestTicketSerializer


class MovementTicketViewSet(viewsets.ModelViewSet):
    queryset = MovementTicket.objects.all()
    serializer_class = MovementTicketSerializer


class ResponsibilityCertificateViewSet(viewsets.ModelViewSet):
    queryset = ResponsibilityCertificate.objects.all()
    serializer_class = ResponsibilityCertificateSerializer
