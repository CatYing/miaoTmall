from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from website.utils import ajax_login_required
from django.contrib import auth
from website.mixin import FrontMixin
import json
import rsa
import random


# Create your views here.


def api_get_public_key(request):
    pass


def api_login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'authenticated': True}), content_type='application/json')
    else:
        if request.method == "POST":
            username = request.POST.get("username", '')
            password_md5 = request.POST.get("password", "")


@login_required(login_url=reverse_lazy("login"))
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class LoginView(FrontMixin, TemplateView):
    template_name = "auth/login.html"

