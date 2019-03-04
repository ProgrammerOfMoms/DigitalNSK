from .models import RecoveryLink
from .serialize import RecoveryLinkSerializer

class LinkGenerator():
    def __init__(self, data):
        serializer = RecoveryLinkSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            self.link = serializer.data["link"]
            self.userId = serializer.data["id"]["id"]
        else:
            self.link = None
            self.userId = -1
        



