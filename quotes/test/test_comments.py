from __future__ import unicode_literals
from httplib import OK, NO_CONTENT, NOT_FOUND
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from quotes.models import Quote, Comment

class FailedAction(Exception):
    def __init__(self, action, response):
        from httplib import responses
        status = responses[response.status_code]
        super(FailedAction, self).__init__(
            '%s action returned %s' % (action.capitalize(), status, ))
        self.response = response

class TestComments(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username = 'author', password = 'password')
        self.commenter = User.objects.create_user(username = 'commenter', password = 'password')
        self.quote = Quote.objects.create(author = self.author, text = 'QUOTE TEXT')

        self._url_create = reverse('quote:comment-create', args = (self.quote.pk, ))
        self._expected_url = reverse('quote:detail', kwargs = {'pk': self.quote.pk, })

        self.client.login(username = 'commenter', password = 'password')

    def test_create(self):
        self._add_comment('YAY')
        self._add_comment('\n'.join(['One line', 'Two lines', ]))

    def test_create_reject_if_empty(self):
        with self.assertRaises(FailedAction):
            self._add_comment('')

        with self.assertRaises(FailedAction):
            self._add_comment('    ')

        with self.assertRaises(FailedAction):
            self._add_comment('\n')

        with self.assertRaises(FailedAction):
            self._add_comment('\n    \n\n   \n    ')

        with self.assertRaises(FailedAction):
            self._add_comment('   \n    \n')

    def test_edit(self):
        comment = self._add_comment('Original')
        self._edit_comment(comment.pk, 'Modified')

    def test_edit_non_existant_comment(self):
        with self.assertRaises(FailedAction) as cm:
            self._edit_comment(1337, 'This should fail')

        self.assertEqual(cm.exception.response.status_code, NOT_FOUND)

    def test_edit_reject_if_empty(self):
        comment = self._add_comment('Original')

        with self.assertRaises(FailedAction):
            self._edit_comment(comment.pk, '')

        with self.assertRaises(FailedAction):
            self._edit_comment(comment.pk, '    ')

        with self.assertRaises(FailedAction):
            self._edit_comment(comment.pk, '\n')

        with self.assertRaises(FailedAction):
            self._edit_comment(comment.pk, '\n    \n\n   \n    ')

        with self.assertRaises(FailedAction):
            self._edit_comment(comment.pk, '   \n    \n')

    def test_delete(self):
        comment = self._add_comment('Original')
        self._delete_comment(comment.pk)

    def test_delete_non_existant_comment(self):
        with self.assertRaises(FailedAction) as cm:
            self._delete_comment(1337)

        self.assertEqual(cm.exception.response.status_code, NOT_FOUND)

    def _add_comment(self, text):
        response = self.client.post(self._url_create, data = {'text': text, })

        if OK != response.status_code:
            raise FailedAction('create', response)

        comment = self.quote.comments.order_by('-created')[0]

        self.assertEqual(comment.text, text)
        self.assertEqual(comment.pk, response.json()['comment_pk'])

        return comment

    def _edit_comment(self, comment_pk, new_text):
        response = self.client.put(
            self._comment_url(comment_pk),
            data = 'text=%s' % (new_text, ))

        if NO_CONTENT != response.status_code:
            raise FailedAction('edit', response)

        comment = Comment.objects.get(pk = comment_pk)

        self.assertEqual(response.status_code, NO_CONTENT)
        self.assertEqual(comment.text, new_text)

    def _delete_comment(self, comment_pk):
        response = self.client.delete(self._comment_url(comment_pk))

        if NOT_FOUND == response.status_code:
            raise FailedAction('delete', response)

        self.assertEqual(response.status_code, NO_CONTENT)
        self.assertFalse(self.quote.comments.filter(pk = comment_pk).exists())

    def _comment_url(self, comment_pk):
        return reverse('quote:comment', kwargs = {
            'pk': self.quote.pk,
            'comment_pk': comment_pk,
        })
