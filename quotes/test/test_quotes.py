from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from quotes.models import Quote

class TestQuotes(TestCase):
    def setUp(self):
        self.silent_bob = User.objects.create_user(
            username = 'sbob',
            password = 'password')

    def test_empty_quote(self):
        with self.assertRaises(ValidationError):
            self.create_quote('')

    def test_single_word_text(self):
        with self.assertRaises(ValidationError):
            self.create_quote('*shrugs*')

    def test_valid_text(self):
        self.create_quote('Shut up.')

    def test_edit_text(self):
        quote = self.create_quote('Do something.')

        quote.text = '*nods*'
        with self.assertRaises(ValidationError):
            quote.full_clean()

        quote.text = ''
        with self.assertRaises(ValidationError):
            quote.full_clean()

    def create_quote(self, text):
        quote = Quote.objects.create(author = self.silent_bob, text = text)
        quote.full_clean()
        return quote
