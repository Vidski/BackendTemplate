from django.contrib.admin.sites import site
from django.views.generic import TemplateView


class CustomView(TemplateView):
    template_name = "../static/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))
        return context