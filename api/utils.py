from django.http import HttpResponseForbidden

class DefaultAuthenticationHandler(object):
    def is_authenticated(self, request):
        return request.user.is_authenticated()

    def challenge(self):
        return HttpResponseForbidden('Only an authenticated user can make the request!')
        