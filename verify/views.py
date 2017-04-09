from django.shortcuts import HttpResponse
from verify.models import *
import random
from PIL import Image, ImageDraw, ImageFont
from tmall.settings import MEDIA_ROOT, HOST
import hashlib, json


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
    image_url = HOST + "/media/code/" + "%s.jpg" % filename.hexdigest()
    new_verify_code = VerifyCode(
        url=image_url,
        available=True,
        code=new_code.__str__()
    )
    new_verify_code.save()
    response = {
        'verify_id': new_verify_code.id,
        'img_url': image_url
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def api_verify(request):
    if request.method == "POST":
        print request.body
        return HttpResponse("2333")
