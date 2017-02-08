from __future__ import unicode_literals
from httplib import NO_CONTENT, BAD_REQUEST
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse, Http404, QueryDict
from django.http import HttpResponseForbidden
from .models import Board, Quote, Comment

try:
    QUOTE_LIST_PAGINATION = settings.QUOTE_LIST_PAGINATION
except AttributeError:
    QUOTE_LIST_PAGINATION = 25

class BoardViewMixin(object):
    @property
    def board(self):
        return Board.objects.get(slug__iexact = self.kwargs.get('board', ''))

    def _get_quote_or_404(self, quote_pk):
        return get_object_or_404(
            self.board.quotes.all(),
            pk = quote_pk)

    def _get_comment_or_404(self, quote_pk, comment_pk):
        return get_object_or_404(
            self._get_quote_or_404(quote_pk).comments.all(),
            pk = comment_pk)

class QuoteList(ListView, BoardViewMixin):
    model = Quote
    template_name = 'quotes/list.html'
    context_object_name = 'quotes'
    paginate_by = QUOTE_LIST_PAGINATION

    def get_queryset(self):
        queryset = super(QuoteList, self).get_queryset() \
            .filter(board__slug__iexact = self.board.slug)

        author = self.request.GET.get('by', None)
        mentions = self.request.GET.get('mentioned', None)

        # Filter by author.
        if author is not None:
            queryset = queryset.filter(author__username__exact = author)

        # Filter by mentioned user.
        if mentions is not None:
            # Split mentioned list and remove any empty items.
            mentions = set(mentions.split(',')) - set([''])
            queryset = queryset.filter(mentions__username__in = mentions).distinct()

        return queryset

@method_decorator(login_required, name = 'dispatch')
class QuoteCreate(CreateView, BoardViewMixin):
    model = Quote
    template_name = 'quotes/create.html'
    fields = ('title', 'text', )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board = self.board
        return super(QuoteCreate, self).form_valid(form)

class QuoteDetail(DetailView, BoardViewMixin):
    model = Quote
    template_name = 'quotes/detail.html'
    context_object_name = 'quote'

@method_decorator(login_required, name = 'dispatch')
class QuoteEdit(UpdateView, BoardViewMixin):
    model = Quote
    template_name = 'quotes/edit.html'
    fields = ('title', 'text', )

@method_decorator(login_required, name = 'dispatch')
class QuoteDelete(DeleteView, BoardViewMixin):
    model = Quote
    success_url = reverse_lazy('index')

class TopQuotes(QuoteList, BoardViewMixin):
    def get_queryset(self):
        queryset = super(TopQuotes, self).get_queryset().annotate(likers_count = Count('likers'))
        return queryset.order_by('-likers_count', '-created')

    def get_context_data(self, **kwargs):
        try:
            return super(TopQuotes, self).get_context_data(**kwargs)
        except Http404:
            # If the user un-liked a quote, the pagination might get screwed up
            # trying to move to the next page. In this case, we reset the page
            # number to 1.
            self.kwargs['page'] = 1
            return super(TopQuotes, self).get_context_data(**kwargs)

class LikeView(View, BoardViewMixin):
    def get(self, request, board, pk):
        quote = self._get_quote_or_404(pk)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

    def put(self, request, board, pk):
        if self.request.user.pk is None:
            return HttpResponseForbidden()

        quote = self._get_quote_or_404(pk)
        quote.likers.add(self.request.user)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

    def delete(self, request, board, pk):
        if self.request.user.pk is None:
            return HttpResponseForbidden()

        quote = self._get_quote_or_404(pk)
        quote.likers.remove(self.request.user)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

class LikersList(TemplateView, BoardViewMixin):
    template_name = 'quotes/likers.html'

    def get_context_data(self, **kwargs):
        context = super(LikersList, self).get_context_data(**kwargs)
        likers = self.request.GET.getlist('likers[]')
        likers = get_user_model().objects.filter(username__in = likers)

        if self.request.user in likers:
            context['liked_by_user'] = True
            context['likers'] = likers.exclude(id = self.request.user.id)
        else:
            context['likers'] = likers

        return context

@method_decorator(login_required, name = 'dispatch')
class Comments(View, BoardViewMixin):
    def post(self, request, board, pk):
        comment_text = self.request.POST['text']

        # It's worth noting we check the stripped version, but save the text as
        # it was given.
        if not comment_text.strip():
            return HttpResponse(status = BAD_REQUEST)

        quote = self._get_quote_or_404(pk)
        comment = quote.comments.create(
            author = self.request.user,
            text = comment_text)

        return JsonResponse({'comment_pk': comment.pk, })

    def put(self, request, board, pk, comment_pk):
        comment = self._get_comment_or_404(pk, comment_pk)
        comment_text = QueryDict(request.body)['text']

        # It's worth noting we check the stripped version, but save the text as
        # it was given.
        if not comment_text.strip():
            return HttpResponse(status = BAD_REQUEST)

        comment.text = comment_text
        comment.save()

        return HttpResponse(status = NO_CONTENT)

    def delete(self, request, board, pk, comment_pk):
        comment = self._get_comment_or_404(pk, comment_pk)
        comment.delete()

        return HttpResponse(status = NO_CONTENT)
