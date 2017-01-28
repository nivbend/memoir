from __future__ import unicode_literals
from django.conf.urls import url

from .views import ProfileView, lookup_view

urlpatterns = [
    url(r'^lookup$', lookup_view, name = 'user-search'),
    url(r'^(?P<username>\w+)$', ProfileView.as_view(), name = 'user-profile'),
]
