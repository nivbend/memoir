from __future__ import unicode_literals
from httplib import OK
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from profiles.templatetags.profiles import profile_link
from quotes.models import Quote

PASSWORD = 'password'

@override_settings(LANGUAGE_CODE = 'en-us', LANGUAGES = (('en', 'English'), ))
class TestLikes(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('author', password = PASSWORD)
        self.quote = Quote.objects.create(author = self.author, text = 'QUOTE TEXT')
        self.url = reverse('quote:like', args = (self.quote.pk, ))

        self.client.login(username = 'author', password = PASSWORD)

    def test_like_and_unlike(self):
        self.assert_likes([])
        self.like()
        self.assert_likes([self.author, ])
        self.unlike()
        self.assert_likes([])

    def test_multiple_likes_for_quote(self):
        self.like()

        another_user = User.objects.create_user('another_user', password = PASSWORD)
        self.client.login(username = 'another_user', password = PASSWORD)

        self.like()
        self.assert_likes([self.author, another_user, ])

    def test_unlike_without_liking(self):
        self.unlike()
        self.assert_likes([])

    def test_attempt_twice(self):
        self.like()
        self.like()
        self.assert_likes([self.author, ])

        self.unlike()
        self.unlike()
        self.assert_likes([])

    def like(self):
        self.client.put(self.url)

    def unlike(self):
        self.client.delete(self.url)

    def assert_likes(self, users):
        self.assertQuerysetEqual(self.quote.likers.all(), map(repr, users), ordered = False)

@override_settings(LANGUAGE_CODE = 'en-us', LANGUAGES = (('en', 'English'), ))
class TestLikersList(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('author', password = PASSWORD)
        self.me = User.objects.create_user('me', password = PASSWORD)
        self.users = [
            User.objects.create_user('user_%d' % (i, ), password = PASSWORD)
            for i in xrange(4)]

        self.quote = Quote.objects.create(author = self.author, text = 'QUOTE TEXT')
        self.url_like = reverse('quote:like', args = (self.quote.pk, ))
        self.url_likers = reverse('quote:likers', args = (self.quote.pk, ))

    def test_you_alone(self):
        self.login('me')
        self.like()
        self.assertHTMLEqual(self.likers(), 'You')

    def test_another(self):
        self.login('user_0')
        self.like()

        self.login('me')
        self.assertHTMLEqual(
            self.likers(),
            profile_link(self.users[0]))

    def test_two_others(self):
        self.login('user_0')
        self.like()
        self.login('user_1')
        self.like()

        self.login('me')
        self.assertHTMLEqual(
            self.likers(),
            '%s and %s' % (
                profile_link(self.users[0]),
                profile_link(self.users[1]),
            ))

    def test_many_others(self):
        self.login('user_0')
        self.like()
        self.login('user_1')
        self.like()
        self.login('user_2')
        self.like()
        self.login('user_3')
        self.like()

        self.login('me')
        self.assertHTMLEqual(
            self.likers(),
            '%s, %s, %s and %s' % (
                profile_link(self.users[0]),
                profile_link(self.users[1]),
                profile_link(self.users[2]),
                profile_link(self.users[3]),
            ))

    def test_you_and_another(self):
        self.login('user_0')
        self.like()

        self.login('me')
        self.like()

        self.assertHTMLEqual(
            self.likers(),
            'You and %s' % (
                profile_link(self.users[0]),
            ))

    def test_you_and_others(self):
        self.login('user_0')
        self.like()
        self.login('user_1')
        self.like()
        self.login('user_2')
        self.like()

        self.login('me')
        self.like()

        self.assertHTMLEqual(
            self.likers(),
            'You, %s, %s and %s' % (
                profile_link(self.users[0]),
                profile_link(self.users[1]),
                profile_link(self.users[2]),
            ))

    def login(self, username):
        self.client.login(username = username, password = PASSWORD)

    def like(self):
        self.client.put(self.url_like)

    def likers(self):
        likers = [user.username for user in self.quote.likers.all()]
        response = self.client.get(self.url_likers, {'likers[]': likers, })
        self.assertEqual(response.status_code, OK)

        return response.getvalue()
