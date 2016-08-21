from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quote

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
