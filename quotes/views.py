from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quote

class QuoteList(ListView):
    model = Quote
    template_name = 'quotes/list.html'
    context_object_name = 'quotes'

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
