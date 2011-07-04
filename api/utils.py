from django.http import HttpResponseRedirect
from django.conf import settings

class DefaultAuthenticationHandler(object):
    def is_authenticated(self, request):
        return request.user.is_authenticated()

    def challenge(self):
        return HttpResponseRedirect(settings.LOGIN_URL)
        

  