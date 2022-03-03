from django.contrib.auth.models import User
from django.test import TestCase

from .models import BasicMediumExpedient
from .libs.utils import generate_num


class BasicMediumExpedientTestCase(TestCase):
    def setUp(self):
        """Setup run before every test method."""
        # Create user for to do the generic test.
        user = User(
            email='testing_login@uci.cu',
            first_name='Testing',
            last_name='Testing',
            username='testing_login',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('admin123')
        user.save()

    def test_create_medium(self):
        # Create 3 Basic Medium
        responsible = User.objects.filter(is_staff=True).first()

        for i in range(3):
            name, inventory_number, location = 'Buro ' + str(i), ('MB' + str(generate_num(7))), 'Laboratorio ' + str(i)

            BasicMediumExpedient.objects.create(name=name, inventory_number=inventory_number,
                                                location=location, responsible=responsible)

        # Check first element if exists
        medium = BasicMediumExpedient.objects.get(name__exact='Buro 0')
        self.assertIsNotNone(medium)
        self.assertEqual(medium.location, 'Laboratorio 0')
        self.assertTrue(medium.is_enable)

        # Check all element if exists
        mediums = BasicMediumExpedient.objects.all()
        self.assertEqual(mediums.count(), 3)
        for obj in mediums:
            self.assertIn('Buro', obj.name)
            self.assertIn('MB', obj.inventory_number)
            self.assertIn('Laboratorio', obj.location)
            self.assertTrue(obj.is_enable)
