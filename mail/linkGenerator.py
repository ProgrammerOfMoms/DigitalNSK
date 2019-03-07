from .models import RecoveryLink
from user.models import User
from .serialize import RecoveryLinkSerializer

import uuid
import random

def linkGenerator(id):
    try:
        user = User.objects.get(id = id)
        link = RecoveryLink.objects.get_or_create(id = user)
        while True:
            h = uuid.uuid4().hex
            if h!=link[0].link:
                link[0].link = h
                # link.save()
                return (link[0].link, user.email)
    except:
        return None
        

    
        



