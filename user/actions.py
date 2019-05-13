from DigitalNSK import settings
from user.models import User

import os
import uuid
import random
import copy
import vk_api

def getPhotoPath(photo, id):
    media_dir = settings.MEDIA_ROOT
    old_photo = ""
    try:
        user = User.objects.get(id = id)
    except User.DoesNotExist:
        return False
    isfirst = True
    if user.photo != "":
        old_photo = user.photo
        isfirst = False
    else:
        while True:
            old_photo = uuid.uuid4().hex
            if old_photo not in os.listdir(media_dir):
                break
    path_to_old_photo = media_dir+"/"+old_photo
    f = open(path_to_old_photo, "wb")
    f.write(photo.read())
    f.close()
    if not isfirst:
            path_to_new_photo = incName(path_to_old_photo)
            os.rename(path_to_old_photo, path_to_new_photo)
            user.photo = path_to_new_photo[path_to_new_photo.rfind('/')+1:]
            user.save()
    else:
        user.photo = old_photo
        user.save()
    
    return user.photo

def incName(photo):
    if photo.find("_") == -1:
        photo = photo + "_1"
    else:
        old_photo = copy.copy(photo)
        start = photo.find("_")
        number = ""
        for i in range(start+1, len(photo)):
            number = number + photo[i]
        if number.isdigit:
            number = int(number) + 1
        number = str(number)
        j = 0
        photo = photo[:start]+"_"+number
    return photo


def auth(token):
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk


    