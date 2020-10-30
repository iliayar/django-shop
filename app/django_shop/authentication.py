from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

import base64

User = get_user_model()

class SingleAdminAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if(len(auth) == 2):
                if auth[0].lower() == 'basic':
                    user, password = base64.b64decode(auth[1]).decode().split(':')
                    if password == settings.ADMIN_PASS:
                        return (User(), None)
        return None
