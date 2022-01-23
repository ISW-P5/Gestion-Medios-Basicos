from django.contrib.auth.models import User
from django.db import models


# TODO: Create Basic Medium Model for relationship with other Models
class Expedient(models.Model):
    """Expediente de Medios Basicos"""
    name = models.CharField(max_length=255, null=False, blank=False,
                            help_text="Nombre del Medio Basico", verbose_name="Nombre")
    inventory_number = models.CharField(max_length=255, null=False, blank=False, verbose_name="Numero de Inventario")
    responsible = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Responsable")
    location = models.CharField(max_length=255, null=False, blank=False,
                                help_text="Ubicacion del Medio Basico", verbose_name="Ubicacion")


class RequestTicket(models.Model):
    """Vale de Solicitud de Medios Basicos"""
    name_requester = models.CharField(max_length=255, null=False, blank=False,
                                      help_text="Nombre del personal que solicita el medio basico",
                                      verbose_name="Nombre del Solicitante")
    basic_medium = models.CharField(max_length=255, null=False, blank=False, verbose_name="Nombre del Medio Basico")
    departament = models.CharField(max_length=255, null=False, blank=False, verbose_name="Departamento")


class MovementTicket(models.Model):
    name_requester = models.CharField(max_length=255, null=False, blank=False,
                                      help_text="Nombre del personal que solicita el medio basico",
                                      verbose_name="Nombre del Solicitante")
    rol_requester = models.CharField(max_length=255, null=False, blank=False,
                                     help_text="Cargo del personal que solicita el medio basico",
                                     verbose_name="Cargo del Solicitante")
    inventory_number = models.CharField(max_length=255, null=False, blank=False, verbose_name="Numero de Inventario")

