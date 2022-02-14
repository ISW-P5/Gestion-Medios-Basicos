from django.contrib import admin

from .models import BasicMediumExpedient, MovementTicket, RequestTicket, ResponsibilityCertificate


# Register your models here.
admin.site.site_header = 'Sistema de Gestion de Medios Basicos'
# TODO: Create basic Admin Django

admin.site.register(BasicMediumExpedient)
admin.site.register(MovementTicket)
admin.site.register(RequestTicket)
admin.site.register(ResponsibilityCertificate)
