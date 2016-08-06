from django.conf.urls import url

from .views import QuoteList, QuoteDetail, QuoteCreate, QuoteEdit, QuoteDelete

urlpatterns = [
    url(r'^$', QuoteList.as_view(), name = 'list'),
    url(r'^create$', QuoteCreate.as_view(), name = 'create'),
    url(r'^(?P<pk>\d+)$', QuoteDetail.as_view(), name = 'detail'),
    url(r'^(?P<pk>\d+)/edit$', QuoteEdit.as_view(), name = 'edit'),
    url(r'^(?P<pk>\d+)/delete$', QuoteDelete.as_view(), name = 'delete'),
]
