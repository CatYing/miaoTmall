from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from website.mixin import FrontMixin
# Create your views here.


class IndexView(FrontMixin, TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("list"))
