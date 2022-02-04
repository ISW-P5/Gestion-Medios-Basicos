from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from .models import BasicMediumExpedient, RequestTicket, MovementTicket, ResponsibilityCertificate
from .serializers import (UserSerializer, BasicMediumExpedientSerializer, RequestTicketSerializer,
                          MovementTicketSerializer, ResponsibilityCertificateSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BasicMediumExpedientViewSet(viewsets.ModelViewSet):
    queryset = BasicMediumExpedient.objects.filter(is_enable=True)
    serializer_class = BasicMediumExpedientSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequestTicketViewSet(viewsets.ModelViewSet):
    queryset = RequestTicket.objects.all()
    serializer_class = RequestTicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovementTicketViewSet(viewsets.ModelViewSet):
    queryset = MovementTicket.objects.all()
    serializer_class = MovementTicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponsibilityCertificateViewSet(viewsets.ModelViewSet):
    queryset = ResponsibilityCertificate.objects.all()
    serializer_class = ResponsibilityCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
