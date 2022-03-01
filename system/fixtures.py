from .models import BasicMediumExpedient
from .libs.utils import generate_num
from django.contrib.auth.models import User


def generate_fixtures(count=100):
    responsible = User.objects.filter(is_staff=True).first()

    for i in range(count):
        name, inventory_number, location = 'Buro ' + str(i), ('MB' + str(generate_num(7))), 'Laboratorio ' + str(i)

        BasicMediumExpedient.objects.create(name=name, inventory_number=inventory_number,
                                            location=location, responsible=responsible)
