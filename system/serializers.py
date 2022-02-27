from collections import OrderedDict

from django.contrib.auth.models import User, Permission, Group
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import MovementTicket, RequestTicket, BasicMediumExpedient, ResponsibilityCertificate


class PageNumberSizePagination(PageNumberPagination):
    """Paginador Personalizado para trabajar con el Frontend"""
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        """Reestructuracion de los datos enviados para que sea compatible con el Frontend"""
        return Response(OrderedDict([
            ('paginator', list(self.page.paginator.page_range)),
            ('page', self.page.number),
            ('per_page', self.page.paginator.per_page),
            ('count', self.page.paginator.count),
            ('items', data)
        ]))


class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializador Simple del Modelo Usuario"""
    role = serializers.SerializerMethodField(label='Rol', allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'role')

    def get_role(self, obj):
        """Devolver nombre del Rol"""
        group = obj.groups.first()
        return group.name if group else None


class UserSerializer(SimpleUserSerializer):
    """Serializador Modelo Usuario"""
    permissions = serializers.SerializerMethodField(label='Permisos', default={})
    role_id = serializers.SerializerMethodField()
    group_id = serializers.IntegerField(write_only=True, required=False)

    class Meta(SimpleUserSerializer.Meta):
        fields = ('url', 'id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                  'group_id', 'role', 'role_id', 'permissions')

        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        """Override Create and add date_joined how now"""
        group = validated_data.get('group_id', 0)
        if group <= 0:
            validated_data.pop('group_id')
        instance = super(UserSerializer, self).create(validated_data)
        instance.date_joined = now()
        # Extract group from data and assign it
        if group > 0:
            instance.groups.set(Group.objects.filter(pk=group))
        # Extract password from data and set password
        password = validated_data.get('password', None)
        if password is not None:
            instance.set_password(password)
        return instance

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        # Extract group from data and assign it
        group = validated_data.get('group_id', 0)
        if group > 0:
            user.groups.set(Group.objects.filter(pk=group))
        try:
            password = validated_data.get('password', None)
            if password is not None:
                user.set_password(password)
                user.save()
        except KeyError:
            pass
        return user

    def get_permissions(self, user):
        """Obtener los permisos del sistema"""
        result = dict()
        # Extraemos todos los permisos
        permissions = Permission.objects.all() if user.is_superuser else \
            user.user_permissions.all() | Permission.objects.filter(group__user=user)
        # Sacamos que modelo y que permiso contiene cada uno
        for permission in permissions.values_list('codename', flat=True):
            action = permission.split('_')[0]
            model = permission[len(action) + 1:]
            # Guardamos el modelo y cada permiso correspondiente
            if model not in result.keys():
                result[model] = [self.get_action_permissions(action)]
            else:
                result[model].append(self.get_action_permissions(action))
        return result

    @staticmethod
    def get_action_permissions(action):
        """Obtenemos los permisos segun el sistema"""
        # Permissions: 0 - View, 1 - Add, 2 - Modify, 3 - Delete, 4 - OWN
        return 0 if action == 'view' else 1 if action == 'add' else 2 if action == 'change' else 3 if action == 'delete' else 4 if action == 'own' else -1

    def get_role_id(self, obj):
        """Devolver el ID del Rol"""
        group = obj.groups.first()
        return group.id if group else 0


class SimpleBasicMediumExpedientSerializer(serializers.ModelSerializer):
    """Serializador Simple Modelo Medio Basico"""

    class Meta:
        model = BasicMediumExpedient
        fields = ('url', 'id', 'name', 'inventory_number', 'responsible', 'location', 'is_enable')
        read_only_fields = ('id',)
        extra_kwargs = {'responsible': {'write_only': True}}


class BasicMediumExpedientSerializer(SimpleBasicMediumExpedientSerializer):
    """Serializador Modelo Medio Basico"""
    owner = SimpleUserSerializer(source='responsible', read_only=True)

    class Meta(SimpleBasicMediumExpedientSerializer.Meta):
        fields = ('url', 'id', 'name', 'inventory_number', 'responsible', 'owner', 'location', 'is_enable')


class RequestTicketSerializer(serializers.ModelSerializer):
    """Serializador Modelo Vale de Solicitud"""
    owner = SimpleUserSerializer(source='requester', read_only=True)
    medium = SimpleBasicMediumExpedientSerializer(source='basic_medium', read_only=True)

    class Meta:
        model = RequestTicket
        fields = ('url', 'id', 'basic_medium', 'medium', 'requester', 'owner', 'departament', 'accepted')
        extra_kwargs = {
            'requester': {'write_only': True},
            'basic_medium': {'write_only': True},
            'accepted': {'required': False}
        }
    
    def create(self, validated_data):
        # Aplicar restricciones del permiso especial
        if (self.context.get('request').user.has_perm('system.own_requestticket') and
                not self.context.get('request').user.is_superuser):
            if validated_data.get('accepted'):
                raise PermissionDenied(detail='Cant create Vale de Solicitud with accepted true!')
            if validated_data.get('requester') != self.context.get('request').user:
                raise PermissionDenied(detail='The requester only can be: ' + self.context.get('request').user.username)
        return super(RequestTicketSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        # Aplicar restricciones del permiso especial
        if (self.context.get('request').user.has_perm('system.own_requestticket') and
                not self.context.get('request').user.is_superuser):
            if validated_data.get('accepted'):
                raise PermissionDenied(detail='Cant update Vale de Solicitud with accepted true!')
            if validated_data.get('requester') != self.context.get('request').user:
                raise PermissionDenied(detail='The requester only can be: ' + self.context.get('request').user.username)
        return super(RequestTicketSerializer, self).update(instance, validated_data)


class MovementTicketSerializer(serializers.ModelSerializer):
    """Serializador Modelo Vale de Movimiento"""
    owner = SimpleUserSerializer(source='requester', read_only=True)
    medium = SimpleBasicMediumExpedientSerializer(source='basic_medium', read_only=True)

    class Meta:
        model = MovementTicket
        fields = ('url', 'id', 'basic_medium', 'medium', 'requester', 'owner', 'actual_location', 'new_location')
        extra_kwargs = {'requester': {'write_only': True}, 'basic_medium': {'write_only': True}}

    def create(self, validated_data):
        # Aplicar restricciones del permiso especial
        if (self.context.get('request').user.has_perm('system.own_movementticket') and
                not self.context.get('request').user.is_superuser):
            if validated_data.get('requester') != self.context.get('request').user:
                raise PermissionDenied(detail='The requester only can be: ' + self.context.get('request').user.username)
        return super(MovementTicketSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # Aplicar restricciones del permiso especial
        if (self.context.get('request').user.has_perm('system.own_movementticket') and
                not self.context.get('request').user.is_superuser):
            if validated_data.get('requester') != self.context.get('request').user:
                raise PermissionDenied(detail='The requester only can be: ' + self.context.get('request').user.username)
        return super(MovementTicketSerializer, self).update(instance, validated_data)


class ResponsibilityCertificateSerializer(serializers.ModelSerializer):
    """Serializador Modelo Acta de Responsabilidad"""
    owner = SimpleUserSerializer(source='responsible', read_only=True)
    medium = SimpleBasicMediumExpedientSerializer(source='basic_medium', read_only=True)

    class Meta:
        model = ResponsibilityCertificate
        fields = ('url', 'id', 'identity_card', 'basic_medium', 'medium', 'responsible', 'owner', 'datetime')
        extra_kwargs = {'responsible': {'write_only': True}, 'basic_medium': {'write_only': True}}
