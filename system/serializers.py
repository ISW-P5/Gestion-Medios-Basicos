from django.contrib.auth.models import User, Permission
from django.utils.timezone import now
from rest_framework import serializers

from .models import MovementTicket, RequestTicket, BasicMediumExpedient, ResponsibilityCertificate


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.SerializerMethodField(label='Rol', allow_null=True)
    permissions = serializers.SerializerMethodField(label='Permisos', default={})

    class Meta:
        model = User
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

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


class BasicMediumExpedientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BasicMediumExpedient
        fields = ('url', 'name', 'inventory_number', 'responsible', 'location')


class RequestTicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequestTicket
        fields = ('url', 'requester', 'basic_medium', 'departament', 'accepted')


class MovementTicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovementTicket
        fields = ('url', 'requester', 'basic_medium', 'actual_location', 'new_location')


class ResponsibilityCertificateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResponsibilityCertificate
        fields = ('url', 'responsible', 'identity_card', 'basic_medium', 'datetime')
