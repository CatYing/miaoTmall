from django.views.generic import TemplateView
from website.mixin import FrontMixin
# Create your views here.


class IndexView(FrontMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
