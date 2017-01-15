from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
from quotes.models import Quote
from ..templatetags.mentions import speakers, references, mentions

class BaseMentionsTestCase(TestCase):
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
        self.kramer.profile.nickname = 'Kramer'
        self.kramer.profile.save()

    def create_quote(self, text):
        return Quote.objects.create(author = self.lerry_david, text = text)

    def assert_mentions(self, quote, speakers):
        self.assertQuerysetEqual(quote.mentions.all(), map(repr, speakers), ordered = False)

class TestSpeakers(BaseMentionsTestCase):
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

class TestReferences(BaseMentionsTestCase):
    def test_one_reference(self):
        quote = self.create_quote('jerry_s: (about @kramer) If you feed him, he\'ll never leave.')

        self.assert_mentions(quote, [self.jerry, self.kramer, ])

    def test_multiple_references(self):
        quote = self.create_quote('frank_c: @george_c, festivus is your heritage!')

        self.assert_mentions(quote, [self.george, ])

        lloyd = User.objects.create_user(
            username = 'lloyd',
            password = 'password')

        quote = self.create_quote('\n'.join([
            '[@kramer, @jerry_s and @lloyd are sitting and chewing gum]',
            'kramer: See, this is what the holidays are all about.',
            ' Three buddies sitting around chewing gum.',
        ]))

        self.assert_mentions(quote, [self.kramer, self.jerry, lloyd, ])

    def test_escaped_reference(self):
        self.assert_mentions(self.create_quote('kramer\\@jerry_s.com'), [])

    def test_unknown_reference(self):
        quote = self.create_quote('\n'.join([
            'newman: Hello, @jerry_s.',
            'jerry_s: Hello, @newman.',
        ]))

        self.assert_mentions(quote, [self.jerry, ])

class TestFilters(BaseMentionsTestCase):
    def setUp(self):
        super(TestFilters, self).setUp()

        self.speaker_jerry = _speaker(self.jerry)
        self.speaker_george = _speaker(self.george)
        self.reference_jerry = _reference(self.jerry)
        self.reference_kramer = _reference(self.kramer)
        self.reference_elaine = _reference(self.elaine)

        self.maxDiff = None

    def test_speakers(self):
        quote = '\n'.join([
            'george_c: You\'ve got to apologize.',
            'jerry_s: Why?',
            'george_c: Because it\'s the mature and adult thing to do.',
            'jerry_s: How does that affect me?',
        ])

        expected_output = '\n'.join([
            '%s You\'ve got to apologize.' % (self.speaker_george, ),
            '%s Why?' % (self.speaker_jerry, ),
            '%s Because it\'s the mature and adult thing to do.' % (self.speaker_george, ),
            '%s How does that affect me?' % (self.speaker_jerry, ),
        ])

        self.assertMultiLineEqual(speakers(quote), expected_output)

    def test_references(self):
        self.assertMultiLineEqual(references('@jerry_s'), self.reference_jerry)

        quote = '\n'.join([
            'elaine_b: Get out!',
            '[@elaine_b pushes on @kramer\'s chest,',
            'causing in to fall backwards through her swinging door]',
        ])

        expected_output = '\n'.join([
            'elaine_b: Get out!',
            '[%s pushes on %s\'s chest,' % (self.reference_elaine, self.reference_kramer, ),
            'causing in to fall backwards through her swinging door]',
        ])

        self.assertMultiLineEqual(references(quote), expected_output)

    def test_mentions(self):
        quote = '\n'.join([
            'george_c: @jerry_s, just remember, it\'s not a lie if you believe it.',
        ])

        expected_output = '\n'.join([
            '%s %s, just remember, it\'s not a lie if you believe it.'
                % (self.speaker_george, self.reference_jerry, ),
        ])

        self.assertMultiLineEqual(mentions(quote), expected_output)

    def test_escaped_reference(self):
        self.assertEqual(references('\@jerry_s'), '&comat;jerry_s')

    def test_nickname(self):
        self.george.profile.nickname = 'T-Bone'
        self.george.profile.save()

        self.assertEqual(speakers('george_c:'), _speaker(self.george, 'T-Bone'))
        self.assertEqual(references('@george_c'), _reference(self.george, 'T-Bone'))

    def test_random_nicknames(self):
        # Short nicknames.
        self.assertEqual(speakers('george_c|T-Bone:'), _speaker(self.george, 'T-Bone'))
        self.assertEqual(references('@george_c|T-Bone'), _reference(self.george, 'T-Bone'))

        # Multi-word nicknames.
        self.assertEqual(speakers('george_c|"Tee Bone":'), _speaker(self.george, 'Tee Bone'))
        self.assertEqual(references('@george_c|"Tee Bone"'), _reference(self.george, 'Tee Bone'))

        # Override existing nicknames.
        self.assertEqual(speakers('kramer|kman:'), _speaker(self.kramer, 'kman'))
        self.assertEqual(references('@kramer|kman'), _reference(self.kramer, 'kman'))
        self.assertEqual(speakers('kramer|"K\' Man":'), _speaker(self.kramer, 'K\' Man'))
        self.assertEqual(references('@kramer|"K\' man"'), _reference(self.kramer, 'K\' man'))

def _speaker(user, nickname = None):
    return ''.join([
        '<strong>',
        '<a class="text-primary" href="/user/%s">' % (user.username, ),
        '%s' % (nickname if nickname else user.first_name, ),
        '</a>:',
        '</strong>',
    ])

def _reference(user, nickname = None):
    return ''.join([
        '<strong>',
        '<a class="text-muted" href="/user/%s">' % (user.username, ),
        '%s' % (nickname if nickname else user.profile.get_name(), ),
        '</a>',
        '</strong>',
    ])
