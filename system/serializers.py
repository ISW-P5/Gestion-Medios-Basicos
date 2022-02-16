from collections import OrderedDict

from django.contrib.auth.models import User, Permission
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import MovementTicket, RequestTicket, BasicMediumExpedient, ResponsibilityCertificate


class PageNumberSizePagination(PageNumberPagination):
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('paginator', list(self.page.paginator.page_range)),
            ('page', self.page.number),
            ('per_page', self.page.paginator.per_page),
            ('count', self.page.paginator.count),
            ('items', data)
        ]))


class SimpleUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(label='Rol', allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'role')

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


class UserSerializer(SimpleUserSerializer):
    permissions = serializers.SerializerMethodField(label='Permisos', default={})

    class Meta(SimpleUserSerializer.Meta):
        fields = ('url', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'permissions')

        # These fields are displayed but not editable and have to be a part of 'fields' tuple
        read_only_fields = ('date_joined',)

        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.date_joined = now()
        return instance

    def get_permissions(self, user):
        result = dict()
        permissions = Permission.objects.all() if user.is_superuser else \
            user.user_permissions.all() | Permission.objects.filter(group__user=user)
        for permission in permissions.values_list('codename', flat=True):
            action = permission.split('_')[0]
            model = permission[len(action) + 1:]
            if model not in result.keys():
                result[model] = [self.get_action_permissions(action)]
            else:
                result[model].append(self.get_action_permissions(action))
        return result

    @staticmethod
    def get_action_permissions(action):
        # Permissions: 0 - View, 1 - Add, 2 - Modify, 3 - Delete
        return 0 if action == 'view' else 1 if action == 'add' else 2 if action == 'change' else 3 if action == 'delete' else -1


class SimpleBasicMediumExpedientSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicMediumExpedient
        fields = ('url', 'id', 'name', 'inventory_number', 'responsible', 'location', 'is_enable')
        read_only_fields = ('id',)
        extra_kwargs = {
            'responsible': {'write_only': True},
        }


class BasicMediumExpedientSerializer(SimpleBasicMediumExpedientSerializer):
    owner = SimpleUserSerializer(source='responsible', read_only=True)

    class Meta(SimpleBasicMediumExpedientSerializer.Meta):
        fields = ('url', 'id', 'name', 'inventory_number', 'responsible', 'owner', 'location', 'is_enable')


class RequestTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestTicket
        fields = ('url', 'requester', 'basic_medium', 'departament', 'accepted')


class MovementTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementTicket
        fields = ('url', 'requester', 'basic_medium', 'actual_location', 'new_location')


class ResponsibilityCertificateSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(source='responsible', read_only=True)
    medium = SimpleBasicMediumExpedientSerializer(source='basic_medium', read_only=True)

    class Meta:
        model = ResponsibilityCertificate
        fields = ('url', 'id', 'identity_card', 'basic_medium', 'medium', 'responsible', 'owner', 'datetime')
        extra_kwargs = {
            'responsible': {'write_only': True},
            'basic_medium': {'write_only': True},
        }
