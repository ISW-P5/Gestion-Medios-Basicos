from django.contrib.auth.models import User
from django.db import models

from system.libs.validators import validate_only_letters, validate_expression, validate_only_letters_numbers


class BasicMediumExpedient(models.Model):
    """Expediente del Medio Basico"""
    name = models.CharField(max_length=255, null=False, blank=False, validators=[validate_only_letters],
                            help_text="Nombre del Medio Basico", verbose_name="Nombre")
    inventory_number = models.CharField(max_length=255, null=False, blank=False, verbose_name="Numero de Inventario",
                                        validators=[validate_expression("[a-zA-Z]{2}\d{7}")])
    responsible = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Responsable")
    location = models.CharField(max_length=255, null=False, blank=False,
                                help_text="Ubicacion del Medio Basico", verbose_name="Ubicacion",
                                validators=[validate_only_letters_numbers])
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")

    class Meta:
        verbose_name = 'Expediente del Medio Basico'
        verbose_name_plural = 'Expedientes de los Medios Basicos'

    def __str__(self):
        return self.inventory_number + ' - ' + self.name


class RequestTicket(models.Model):
    """Vale de Solicitud del Medio Basico"""
    requester = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                                  help_text="Personal que solicita el medio basico",
                                  verbose_name="Solicitante")
    basic_medium = models.ForeignKey(BasicMediumExpedient, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name='Medio Basico')
    departament = models.CharField(max_length=255, null=False, blank=False, verbose_name="Departamento")
    accepted = models.BooleanField(default=False, verbose_name='Esta Aceptado el Vale')

    class Meta:
        verbose_name = 'Vale de Solicitud'
        verbose_name_plural = 'Vales de Solicitud'

    def __str__(self):
        return self.requester.first_name + ' - ' + self.basic_medium.name


class MovementTicket(models.Model):
    """Vale de Movimiento del Medio Basico"""
    requester = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE,
                                  help_text="Personal que solicita el medio basico",
                                  verbose_name="Solicitante")
    basic_medium = models.ForeignKey(BasicMediumExpedient, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name='Medio Basico')
    actual_location = models.CharField(max_length=255, null=False, blank=False, verbose_name='Ubicacion Actual',
                                       validators=[validate_only_letters])
    new_location = models.CharField(max_length=255, null=False, blank=False, verbose_name='Ubicacion Nueva',
                                    validators=[validate_only_letters])

    class Meta:
        verbose_name = 'Vale de Movimiento'
        verbose_name_plural = 'Vales de Movimiento'

    def __str__(self):
        return self.requester.first_name + ' - ' + self.basic_medium.name


class ResponsibilityCertificate(models.Model):
    """Acta de Responsabilidad del Medio Basico"""
    responsible = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Responsable")
    identity_card = models.CharField(max_length=20, null=False, blank=False,
                                     validators=[validate_expression("^\d{11}$")],
                                     verbose_name='Carnet de Identidad')
    basic_medium = models.ForeignKey(BasicMediumExpedient, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name='Medio Basico')
    datetime = models.DateTimeField(auto_now=True, auto_created=True, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Acta de Responsabilidad'
        verbose_name_plural = 'Actas de Responsabilidad'

    def __str__(self):
        return self.responsible.first_name + ' - ' + self.basic_medium.name
