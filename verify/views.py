# coding=utf8
from django.shortcuts import HttpResponse
from verify.models import *
import random
from PIL import Image, ImageDraw, ImageFont
from tmall.settings import MEDIA_ROOT, HOST
import hashlib, json
import base64


# Create your views here.

def api_generate_code(request):
    new_code = random.randrange(1000, 10000)
    image = Image.new("RGB", (147, 49), color=(255, 255, 255))
    font_file = MEDIA_ROOT + "/ttf/Roboto-Regular.ttf"
    font = ImageFont.truetype(font_file, 47)
    draw = ImageDraw.Draw(image)
    draw.text((7, 0), new_code.__str__(), fill=(0, 0, 0), font=font)
    del draw
    filename = hashlib.md5()
    filename.update(new_code.__str__())
    image.save(MEDIA_ROOT + "/code/" + "%s.jpg" % filename.hexdigest())
    new_verify_code = VerifyCode(
        available=True,
        code=new_code.__str__(),
    )
    new_verify_code.save()
    fp = open(MEDIA_ROOT + "/code/" + "%s.jpg" % filename.hexdigest(), "rb")
    response = {
        'verify_id': new_verify_code.id,
        'img_base64': base64.b64encode(fp.read()),
    }
    fp.close()
    return HttpResponse(json.dumps(response), content_type="application/json")


def api_verify(request):
    if request.method == "POST":
        verify_id = request.POST.get("id", "")
        verify_code = request.POST.get("code", "")
        if VerifyCode.objects.filter(id=int(verify_id)).count() == 0:
            return HttpResponse(json.dumps({'result': 0, "message": "不存在验证码"}), content_type='application/json')
        else:
            code = VerifyCode.objects.get(id=int(verify_id))
            if not code.available:
                return HttpResponse(json.dumps({'result': 0, "message": "验证码失效"}), content_type='application/json')
            else:
                if code.code != verify_code:
                    return HttpResponse(json.dumps({'result': 0, 'message': "验证码错误"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'result': 1}), content_type='application/json')
