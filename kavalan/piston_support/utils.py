# Custom utility classes and functions for using Piston
from piston.utils import rc
from piston.resource import Resource

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

class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)