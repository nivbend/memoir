from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic import View, DetailView
from .models import UserProfile

@method_decorator(login_required, name = 'dispatch')
class ProfileView(DetailView):
    template_name = 'profiles/user_detail.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        """Lookup profile by their associated users."""
        return get_user_model().objects.all()

    def get_object(self, queryset = None):
        # Pass the profile object to the template, not the User.
        return super(ProfileView, self).get_object(queryset).profile

def lookup_view(request):
    name = request.GET['q']

    query = Q()
    for word in name.split(' '):
        if not word.strip():
            continue

        query |= Q(first_name__icontains = word)
        query |= Q(last_name__icontains = word)

    users = get_user_model().objects.filter(query)

    return JsonResponse({
        'matches': [{
                'username': u.username,
                'full_name': u.get_full_name(),
            }
            for u in users],
    })
