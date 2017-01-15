"""Memoir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name = 'quote:top'), name = 'index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', auth_views.login, {'template_name': 'profiles/login.html', }, name = 'login'),
    url(r'^switch_user$', auth_views.logout_then_login, name = 'switch-user'),
    url(r'^user/', include('profiles.urls')),
    url(r'^quote/', include('quotes.urls', namespace = 'quote')),
]
