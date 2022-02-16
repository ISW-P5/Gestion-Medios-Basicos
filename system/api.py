import json
from abc import abstractmethod

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets

from .models import BasicMediumExpedient, RequestTicket, MovementTicket, ResponsibilityCertificate
from .serializers import (UserSerializer, BasicMediumExpedientSerializer, RequestTicketSerializer,
                          MovementTicketSerializer, ResponsibilityCertificateSerializer)


class FilterViewSetMixin(viewsets.ModelViewSet):
    def filter_queryset(self, queryset):
        filters = self.request.GET.get('filter', None)
        try:
            ordering = json.loads(self.request.GET.get('ordering', {'asc': True, 'column': 'id'}))
        except Exception:  # Dont can read ordering data (because is not a json)
            ordering = {'asc': True, 'column': 'id'}
        if filters is not None and filters != '':
            queryset = self.get_filter(queryset, filters)
        return queryset.order_by(('-' if not ordering.get('asc') else '') + ordering.get('column'))

    @abstractmethod
    def get_filter(self, queryset, value):
        return queryset


class UserViewSet(FilterViewSetMixin):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_filter(self, queryset, value):
        return queryset.filter(Q(username__contains=value) | Q(first_name__contains=value) |
                               Q(last_name__contains=value)).order_by('-date_joined')


class BasicMediumExpedientViewSet(FilterViewSetMixin):
    queryset = BasicMediumExpedient.objects.all()
    serializer_class = BasicMediumExpedientSerializer

    def get_filter(self, queryset, value):
        return queryset.filter(Q(name__contains=value) |
                               Q(inventory_number__contains=value) |
                               Q(location__contains=value))


class RequestTicketViewSet(FilterViewSetMixin):
    queryset = RequestTicket.objects.all()
    serializer_class = RequestTicketSerializer

    def get_filter(self, queryset, value):
        return super(RequestTicketViewSet, self).get_filter(queryset, value)


class MovementTicketViewSet(FilterViewSetMixin):
    queryset = MovementTicket.objects.all()
    serializer_class = MovementTicketSerializer

    def get_filter(self, queryset, value):
        return super(MovementTicketViewSet, self).get_filter(queryset, value)


class ResponsibilityCertificateViewSet(FilterViewSetMixin):
    queryset = ResponsibilityCertificate.objects.filter(basic_medium__is_enable=True)
    serializer_class = ResponsibilityCertificateSerializer

    def get_filter(self, queryset, value):
        return queryset.filter(Q(identity_card__contains=value) |
                               Q(basic_medium__inventory_number__contains=value) |
                               Q(basic_medium__name__contains=value) |
                               Q(responsible__username__contains=value))
