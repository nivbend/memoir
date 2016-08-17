from django.conf.urls import url

from .views import ProfileView

urlpatterns = [
    url(r'^(?P<username>\w+)$', ProfileView.as_view(), name = 'user-profile'),
]
