from django.views.generic import DetailView,ListView,View

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Person

class ProfileDetailView(DetailView):

    model = Person
    template_name="accounts/profile.html"
    context_object_name = 'person'
    slug_field = "username"


class MyAccountView(LoginRequiredMixin,DetailView):

    model = Person
    template_name="accounts/my_account.html"
    context_object_name = 'my'

    def get_object(self,queryset=None):
        return self.request.user