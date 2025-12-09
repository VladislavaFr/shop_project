from django.test import TestCase

class DummyTest(TestCase):
    def test_ok(self):
        self.assertEqual(1, 1)