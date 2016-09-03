from django.conf.urls import url

from .views import QuoteList, QuoteDetail, QuoteCreate, QuoteEdit, QuoteDelete
from .views import TopQuotes, LikeView, LikersList, Comments

urlpatterns = [
    url(r'^$', QuoteList.as_view(), name = 'list'),
    url(r'^top$', TopQuotes.as_view(), name = 'top'),
    url(r'^create$', QuoteCreate.as_view(), name = 'create'),
    url(r'^(?P<pk>\d+)$', QuoteDetail.as_view(), name = 'detail'),
    url(r'^(?P<pk>\d+)/edit$', QuoteEdit.as_view(), name = 'edit'),
    url(r'^(?P<pk>\d+)/delete$', QuoteDelete.as_view(), name = 'delete'),
    url(r'^(?P<pk>\d+)/like$', LikeView.as_view(), name = 'like'),
    url(r'^(?P<pk>\d+)/likers$', LikersList.as_view(), name = 'likers'),
    url(r'^(?P<pk>\d+)/comment$', Comments.as_view(), name = 'comment-create'),
    url(r'^(?P<pk>\d+)/comment/(?P<comment_pk>\d+)$', Comments.as_view(), name = 'comment'),
]
