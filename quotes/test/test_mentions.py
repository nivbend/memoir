from django.contrib.auth.models import User
from django.test import TestCase
from quotes.models import Quote

class TestSpeakers(TestCase):
    def setUp(self):
        self.lerry_david = User.objects.create_user(
            username = 'lerry_david',
            password = 'password')

        self.jerry = User.objects.create_user(
            username = 'jerry_s',
            password = 'password',
            first_name = 'Jerry',
            last_name = 'Seinfeld')

        self.george = User.objects.create_user(
            username = 'george_c',
            password = 'password',
            first_name = 'George',
            last_name = 'Costanza')

        self.elaine = User.objects.create_user(
            username = 'elaine_b',
            password = 'password',
            first_name = 'Elaine',
            last_name = 'Benes')

        self.kramer = User.objects.create_user(
            username = 'kramer',
            password = 'password',
            first_name = 'Cosmo',
            last_name = 'Kramer')

    def test_empty_text(self):
        quote = self.create_quote('')

        self.assert_mentions(quote, [])

    def test_no_speakers(self):
        quote = self.create_quote('Nobody is mentioned!')

        self.assert_mentions(quote, [])

    def test_single_speaker(self):
        quote = self.create_quote('kramer: Boy, these pretzels are makin\' me thirsty.')

        self.assert_mentions(quote, [self.kramer, ])

    def test_multiple_speakers(self):
        quote = self.create_quote('\n'.join([
            'kramer: The bus is outta control.',
            ' So I grab him by the collar, I take him out of the seat,',
            ' I get behind the wheel, and now I\'m driving the bus.',
            'jerry_s: Wow.',
            'george_c: You\'re Batman.',
            'kramer: Yeah, yeah, I am Batman.',
            ' Then the mugger, he comes to and he starts choking me.',
            ' So I\'m fighting him off with one hand and I kept driving the bus with the',
            ' other, ya know. Then I managed to open up the door and I kicked him out the',
            ' door, ya know, with my foot, ya know, at the next stop.',
            'jerry_s: You kept making all the stops?',
            'kramer: Well, people kept ringing the bell!',
        ]))

        self.assert_mentions(quote, [self.jerry, self.george, self.kramer, ])

    def test_unknown_speaker(self):
        quote = self.create_quote('\n'.join([
            'jerry_s: I wanted to talk to you about Dr. Whatley.',
            ' I have a suspicion that he\'s converted to Judaism purely for the jokes.',
            'priest: And this offends you as a Jewish person?',
            'jerry_s: No, it offends me as a comedian.',
        ]))

        self.assert_mentions(quote, [self.jerry, ])

    def test_update(self):
        quote = self.create_quote(
            'kramer: When you look annoyed all the time, people think that you\'re busy')

        self.assert_mentions(quote, [self.kramer, ])

        # Fix speaker.
        quote.text = 'george_c: When you look annoyed all the time, people think that you\'re busy'
        quote.save()

        self.assert_mentions(quote, [self.george, ])

    def test_delete_quote(self):
        quote_1 = self.create_quote(
            'george_c: Jerry, just remember, it\'s not a lie if you believe it.')
        quote_2 = self.create_quote(
            'george_c: My name is George, I\'m unemployed and I live with my parents.')

        self.assertIn(quote_1, self.george.mentioned_in.all())
        quote_1.delete()
        self.assertQuerysetEqual(self.george.mentioned_in.all(), [repr(quote_2), ])
        quote_2.delete()
        self.assertQuerysetEqual(self.george.mentioned_in.all(), [])

    def create_quote(self, text):
        return Quote.objects.create(author = self.lerry_david, text = text)

    def assert_mentions(self, quote, speakers):
        self.assertQuerysetEqual(quote.mentions.all(), map(repr, speakers), ordered = False)
