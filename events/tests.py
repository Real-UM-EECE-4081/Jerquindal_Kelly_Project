from django.test import TestCase
from events.models import TrainingSite


class TrainingTestCase(TestCase):
    def setUp(self):
        TrainingSite.objects.create(name='HaydenHall', address='3795 Desoto', zip_code='38152', phone='123-45-6789',
                                    owner='1')


class EventTestCase(TestCase):
    def setUp(self):
        TrainingSite.objects.create(name='HaydenHall', address='3795 Desoto', zip_code='38152', phone='123-45-6789',
                                    owner='1')
