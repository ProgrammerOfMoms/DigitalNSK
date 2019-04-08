from DigitalNSK import settings
from user.models import User

import os
import uuid
import random

def getPhotoPath(photo, id):
    media_dir = settings.MEDIA_ROOT
    old_photo = ""
    try:
        user = User.objects.get(id = id)
    except User.DoesNotExist:
        return False
    if user.photo != "":
        old_photo = user.photo
    else:
        while True:
            old_photo = uuid.uuid4().hex
            if old_photo not in os.listdir(media_dir):
                break
    f = open(f"{media_dir}/{old_photo}", "wb")
    f.write(photo.read())
    f.close()
    if user.photo!=old_photo:
        user.photo = old_photo
        user.save()
    return True
    