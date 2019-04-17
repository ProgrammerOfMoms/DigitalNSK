import os
import uuid
import random
import copy
import base64

f = open("/home/dato/Изображения/1.png", "rb")
photo = f.read()
print(base64.b64decode(photo))

