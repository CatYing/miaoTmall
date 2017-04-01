from django.http import HttpResponse
from django.shortcuts import render
from website.utils import ajax_login_required
import json
import rsa

# Create your views here.


def get_public_key(request):
    pass


def login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'authenticated': True}), content_type='application/json')
    else:
        if request.method == "POST":
            username = request.POST.get("username", '')
            password_md5 = request.POST.get("password", "")
