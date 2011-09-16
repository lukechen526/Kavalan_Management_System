from piston.utils import rc

class SessionAuthenticationHandler(object):
    """
    Authenticates the user based on the built-in session framework.
    Note that this is NOT RESTful, but it does simplify the application. For APIs that are meant only for internal use,
    this is a reasonable trade-off.
    """
    def is_authenticated(self, request):
        return request.user.is_authenticated()

    def challenge(self):
        return rc.FORBIDDEN
        