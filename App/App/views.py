from django.contrib.admin.sites import site
from django.views.generic import TemplateView


class CustomView(TemplateView):
    """
    This is a custom view included just to add a new page into
    the admin site. It can be removed if you don't need it, but
    take in mind that you will need to remove or comment the
    function `manageHomePage` in the file `App/Static/admin_js.js`,
    and `CustomView` in the App/urls.py file.
    """

    template_name = '../static/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))
        return context
