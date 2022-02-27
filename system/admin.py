from django.contrib import admin

from .models import BasicMediumExpedient, MovementTicket, RequestTicket, ResponsibilityCertificate


# Renombrar titulo del Panel Administrativo de Django
admin.site.site_header = 'Sistema de Gestion de Medios Basicos'

# Registrar Modelos sin especificar el AdminModel
admin.site.register(BasicMediumExpedient)
admin.site.register(MovementTicket)
admin.site.register(RequestTicket)
admin.site.register(ResponsibilityCertificate)
