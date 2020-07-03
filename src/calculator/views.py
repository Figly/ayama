from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic



class ShowCalcs(LoginRequiredMixin, generic.TemplateView):
    template_name = "calculator/index.html"
    http_method_names = ["get"]

    def get(self, request):
        slug = self.kwargs.get("slug")
        if slug:
            profile = get_object_or_404(models.Profile, slug=slug)
            user = profile.user
        else:
            user = self.request.user

        return super().get(request)