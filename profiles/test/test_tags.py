from django.contrib.auth.models import User
from django.test import TestCase
from ..templatetags.profiles import profile_link

class TestLink(TestCase):
    def setUp(self):
        self.bob = User.objects.create_user(
            username = 'rastaman45',
            password = '850511')

    def test_lean_user(self):
        self.assert_link('rastaman45')

    def test_first_name(self):
        self.bob.first_name = 'Robert'

        self.assert_link('Robert')

    def test_full_name(self):
        self.bob.first_name = 'Robert'
        self.bob.middle_name = 'Nesta'
        self.bob.last_name = 'Marley'

        self.assert_link('Robert')

    def test_nickname(self):
        self.bob.profile.nickname = 'Bob'

        self.assert_link('Bob')

    def test_classes(self):
        self.bob.profile.nickname = 'Bob'

        self.assertEqual(
            profile_link(self.bob, classes = ''),
            '<a class="" href="/user/%s">Bob</a>' % (self.bob.username, ))

        self.assertEqual(
            profile_link(self.bob, classes = 'some-class'),
            '<a class="some-class" href="/user/%s">Bob</a>' % (self.bob.username, ))

        self.assertEqual(
            profile_link(self.bob, classes = 'text-primary hidden'),
            '<a class="text-primary hidden" href="/user/%s">Bob</a>' % (self.bob.username, ))

    def assert_link(self, name):
        expected = '<a class="" href="/user/%s">%s</a>' % (self.bob.username, name, )
        self.assertEqual(profile_link(self.bob), expected)
