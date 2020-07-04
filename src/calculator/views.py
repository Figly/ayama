from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from profiles.models import Profile


class ShowCalcs(LoginRequiredMixin, generic.TemplateView):
    template_name = "calculator/index.html"
    http_method_names = ["get"]

    def get(self, request):
        slug = self.kwargs.get("slug")
        if slug:
            profile = get_object_or_404(Profile, slug=slug)
            user = profile.user  # noqa
        else:
            user = self.request.user  # noqa

        return super().get(request)
