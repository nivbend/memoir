from __future__ import unicode_literals
from httplib import NO_CONTENT, BAD_REQUEST
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse, Http404, QueryDict
from django.http import HttpResponseForbidden
from .models import Quote, Comment

class QuoteList(ListView):
    model = Quote
    template_name = 'quotes/list.html'
    context_object_name = 'quotes'

    def get_queryset(self):
        queryset = super(QuoteList, self).get_queryset()

        author = self.request.GET.get('by', None)
        mentions = self.request.GET.get('mentioned', None)
        limit = self.request.GET.get('limit', None)

        # Filter by author.
        if author is not None:
            queryset = queryset.filter(author__username__exact = author)

        # Filter by mentioned user.
        if mentions is not None:
            # Split mentioned list and remove any empty items.
            mentions = set(mentions.split(',')) - set([''])
            queryset = queryset.filter(mentions__username__in = mentions).distinct()

        # Limit number of results.
        if limit is not None:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass

        return queryset

@method_decorator(login_required, name = 'dispatch')
class QuoteCreate(CreateView):
    model = Quote
    template_name = 'quotes/create.html'
    fields = ('title', 'text', )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuoteCreate, self).form_valid(form)

class QuoteDetail(DetailView):
    model = Quote
    template_name = 'quotes/detail.html'
    context_object_name = 'quote'

@method_decorator(login_required, name = 'dispatch')
class QuoteEdit(UpdateView):
    model = Quote
    template_name = 'quotes/edit.html'
    fields = ('title', 'text', )

@method_decorator(login_required, name = 'dispatch')
class QuoteDelete(DeleteView):
    model = Quote
    success_url = reverse_lazy('index')

class TopQuotes(QuoteList):
    def get_queryset(self):
        queryset = super(TopQuotes, self).get_queryset().annotate(likers_count = Count('likers'))
        return queryset.order_by('-likers_count', '-created')

class LikeView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk = pk)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

    def put(self, request, pk):
        if self.request.user.pk is None:
            return HttpResponseForbidden()

        quote = get_object_or_404(Quote, pk = pk)
        quote.likers.add(self.request.user)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

    def delete(self, request, pk):
        if self.request.user.pk is None:
            return HttpResponseForbidden()

        quote = get_object_or_404(Quote, pk = pk)
        quote.likers.remove(self.request.user)
        return JsonResponse({'likers': map(str, quote.likers.all()), })

class LikersList(TemplateView):
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
class Comments(View):
    def post(self, request, pk):
        comment_text = self.request.POST['text']

        # It's worth noting we check the stripped version, but save the text as
        # it was given.
        if not comment_text.strip():
            return HttpResponse(status = BAD_REQUEST)

        quote = get_object_or_404(Quote, pk = pk)
        comment = quote.comments.create(
            author = self.request.user,
            text = comment_text)

        return JsonResponse({'comment_pk': comment.pk, })

    def put(self, request, pk, comment_pk):
        comment = _get_comment_or_404(pk, comment_pk)
        comment_text = QueryDict(request.body)['text']

        # It's worth noting we check the stripped version, but save the text as
        # it was given.
        if not comment_text.strip():
            return HttpResponse(status = BAD_REQUEST)

        comment.text = comment_text
        comment.save()

        return HttpResponse(status = NO_CONTENT)

    def delete(self, request, pk, comment_pk):
        comment = _get_comment_or_404(pk, comment_pk)

        comment.delete()

        return HttpResponse(status = NO_CONTENT)

def _get_comment_or_404(quote_pk, comment_pk):
    quote = get_object_or_404(Quote, pk = quote_pk)
    comment = quote.comments.filter(pk = comment_pk)

    if not comment.exists():
        raise Http404()

    return comment.get()
