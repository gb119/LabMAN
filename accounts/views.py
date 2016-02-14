from django.views.generic import DetailView,ListView
from django.core.exceptions import ObjectDoesNotExist
from .models import Person
from tagged_object.models import CategoryLabels
from img.models import ImageFile
from pages.models import Page
from datetime import date
from django.contrib.sites.shortcuts import get_current_site


class ProfileDetailView(DetailView):

    model = Person
    template_name="accounts/profile.html"
    context_object_name = 'person'
    slug_field = "username"

    def get_context_data(self, **kwargs):

        context=super(ProfileDetailView,self).get_context_data(**kwargs)
        site = get_current_site(self.request)
        profile=CategoryLabels.objects.get(name="profile")
        this = self.get_object()
        try:
            image=this.images.get(category=profile,tag=this.username)
        except ObjectDoesNotExist:
            image=ImageFile.objects.get(category=profile,tag="default")

        try:
            page=this.pages.get(category=profile,tag=this.username)
        except ObjectDoesNotExist:
            page=Page.objects.create(title=this.display_name,category=profile,tag=this.username,published=date.today(),
                                     owner=this,content_type=Person,content_object=this)
            page.sites.add(site)
            page.save()

        context["profile_image"]=image
        context["profile_page"]=page
        return context