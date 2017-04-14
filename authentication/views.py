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
import os
import base64

# Create your views here.


def api_get_public_key(request):
    with open(os.path.dirname(__file__) + '/public.pem', 'r') as public_file:
        public_string = public_file.read().strip()
    result = {
        "public": public_string
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def api_login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'authenticated': True}), content_type='application/json')
    else:
        if request.method == "POST":
            encrypt_info_base64 = request.POST.get("info")
            with open(os.path.dirname(__file__) + '/private.pem', "r") as fp:
                key_data = fp.read()
            private_key = rsa.PrivateKey.load_pkcs1(key_data)
            encrypt_info = base64.b64decode(encrypt_info_base64)
            message = rsa.decrypt(encrypt_info, private_key)
            message_dict = json.loads(message)
            username = message_dict['username'][:-4]
            password = message_dict['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponse("666")
            else:
                pass


@login_required(login_url=reverse_lazy("login"))
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class LoginView(FrontMixin, TemplateView):
    template_name = "auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect("index")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

