from piston.utils import rc

class DefaultAuthenticationHandler(object):
    def is_authenticated(self, request):
        return request.user.is_authenticated()

    def challenge(self):
        return rc.FORBIDDEN
        