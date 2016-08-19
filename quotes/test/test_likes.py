from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from quotes.models import Quote

class TestLikes(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('author', password = 'password')
        self.quote = Quote.objects.create(author = self.author, text = 'QUOTE TEXT')
        self.url = reverse('quote:like', args = (self.quote.pk, ))

        self.client.login(username = 'author', password = 'password')

    def test_like_and_unlike(self):
        self.assert_likes([])
        self.like()
        self.assert_likes([self.author, ])
        self.unlike()
        self.assert_likes([])

    def test_multiple_likes_for_quote(self):
        self.like()

        another_user = User.objects.create_user('another_user', password = 'password')
        self.client.login(username = 'another_user', password = 'password')

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
