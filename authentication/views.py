# coding=utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from website.utils import ajax_login_required
from django.contrib import auth
from website.mixin import FrontMixin
import json
import rsa
import os
import base64
from authentication.models import *
from verify.models import *


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
            verify_id = int(message_dict['id'])
            verify_code = username[-4:]
            if not VerifyCode.objects.get(id=verify_id).available:
                pass
            elif VerifyCode.objects.get(id=verify_id).code != verify_code:
                pass
            else:
                VerifyCode.objects.get(id=verify_id).available = False
                VerifyCode.objects.get(id=verify_id).save()
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponse("666")
            else:
                pass


@login_required(login_url=reverse_lazy('login'))
def switch(request):
    stage = int(request.GET.get("stage", ""))
    if stage == 1:
        request.user.myuser.current_stage = 1
        request.user.myuser.save()
        return HttpResponseRedirect(reverse_lazy("index"))
    else:
        if request.user.myuser.level >= stage:
            request.user.myuser.current_stage = stage
            request.user.myuser.save()
        return HttpResponseRedirect(reverse_lazy("index"))



@login_required(login_url=reverse_lazy("login"))
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class LoginView(FrontMixin, TemplateView):
    template_name = "auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy("index"))
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)


class RegisterView(FrontMixin, TemplateView):
    template_name = "auth/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy("index"))
        else:
            if request.method == "POST":
                print request.POST
                username = request.POST.get("username")
                if User.objects.filter(username=username).count() != 0:
                    return HttpResponse("该手机已注册")
                else:
                    password = request.POST.get("password", "")
                    nickname = request.POST.get("nickname", "")
                    name = request.POST.get("name", "")
                    identity = request.POST.get("identity", "")
                    head_img = request.FILES.get("head")

                    new_user = User.objects.create_user(
                        username=username,
                        password=password,
                    )
                    new_user.save()

                    new_real_info = RealInfo(
                        real_name=name,
                        id_number=identity
                    )
                    new_real_info.save()

                    new_my_user = MyUser(
                        user=new_user,
                        nickname=nickname,
                        cellphone=username,
                        real_info=new_real_info,
                        head_img=head_img
                    )
                    new_my_user.save()

                    auth.login(request, new_user)
                    return HttpResponseRedirect(reverse_lazy("index"))
            else:
                return super(RegisterView, self).dispatch(request, *args, **kwargs)

