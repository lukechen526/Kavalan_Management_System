from piston.handler import BaseHandler
from piston.utils import *
from hermes.models import MessageThread, Message, ThreadParticipation, ThreadOwnership, UserHAuthParameters
from django.conf import settings
from django.http import HttpResponseBadRequest, QueryDict
import random
import string
import hmac, hashlib
from urllib import quote_plus
import binascii

#WARNING!
#It is expected that all request will be conducted via https

class RequestKeySecretPairHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = UserHAuthParameters
    fields = ('key', 'secret')

    @classmethod
    def create(self, request):
        user = request.user
        key, secret = self.generate_key_secret_pair()
        pair, created = UserHAuthParameters.objects.get_or_create(user=user)
        pair.key, pair.secret = key, secret
        pair.save()
        return pair
    
    def generate_key_secret_pair(self, length=30):
        """
        Generates a random key/secret key pair in the form of two alphanumeric strings of the specified length
        :param length: length of the string to be generated. Default = 30
        :return: a tuple of (key, secret)
        """
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
        secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
        return key, secret



class CreateThreadHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = MessageThread
    fields = ('pk', 'subject', 'creator', 'last_updated')
    
    @classmethod
    def create(self, request):
        if (('subject' in request.POST and request.POST['subject']) and
            ('creator' in request.POST and request.POST['creator'])
            ):
            pass
        else:
            resp = rc.BAD_REQUEST.write('Needs to have a subject!')

            


class JoinThreadHandler(BaseHandler):
    allowed_methods = ('POST', )
    model = ThreadParticipation
    fields = ('user', 'thread' )


def escape(s):
    return quote_plus(s, safe='~')

class HAuthenticationHandler(object):
    """
    Implements a OAuth-like, but more lightweight protocol for authentication/authorization in Hermes.
    The client will request the key/secret pair from the server directly. The key/secret pair then allows the client to
    sign its requests and pass it to a third-party (e.g. a Node.js+Socket.io server) for delivery.
    """
    def is_authenticated(self, request):
        #Validates that the request has all the necessary HAuth parameters and
        #
        if not self.is_valid_request(request):
            return False
        
        #Verifies the signature
        if not self.verify_signature(request):
            return False
        
        




    def is_valid_request(self, request):

        must_have = [ 'hauth_' + s for s in ['key', 'signature', 'timestamp', 'nonce', 'signature_method']]
        is_in = lambda l: all([ (p in l) for p in must_have ])
        auth_params = request.META.get('AUTHORIZATION', '')
        req_params = request.REQUEST
             
        if not is_in(auth_params) and  not is_in(req_params):
            return False

        #Checks the timestamp and the nonce


    def verify_signature(self, request):
        """
        Verifies the HAuth signature
        Required hauth parameters in the request:

        hauth_key: the key that identifies the user
        hauth_timestamp: the timestamp = the number of seconds since January 1, 1970 00:00:00 GMT
        hauth_nonce: a random string of <= 30 characters, generated PER REQUEST
        hauth_signature_method: 'HMAC-SHA1' or 'HMAC-MD5'
        hauth_signature: the HMAC signature of the request using the specified method. Similar to OAuth. Check

        :param request: the HttpRequest object
        :return: True if the verification succeeds, False if not.
        """

        auth_params = request.META.get('AUTHORIZATION', '')
        req_params = request.REQUEST
        all_params = req_params.copy()
        all_params.update(auth_params)
        all_params = all_params.dict()

        hauth_signature = all_params.pop('hauth_signature')
        hauth_signature_method = all_params.get('hauth_signature_method')

        user_key = all_params.get('hauth_key')
        
        #Tries retrieving the secret
        try:
            user = UserHAuthParameters.objects.get(key=user_key)
            user_secret = escape(user.secret)
        except UserHAuthParameters.DoesNotExist:
            return False

        #Verifies that the timestamp and nonce are value before checking the signature
        hauth_timestamp = all_params['hauth_timestamp']
        hauth_nonce = all_params['hauth_nonce']

        if int(hauth_timestamp) < int(user.last_timestamp):
            return False
        if hauth_nonce == user.last_nonce:
            return False

        #Checks if the calculated signature is identical to the one sent in the request
        #Sorts the keys of all_params and generate the string with normalized request parameters. All parameters
        #need to be encoded in UTF-8 first, the URL-escaped.
        
        normalized_string = '&'.join(['%s=%s' % (escape(key), escape(all_params[key])) for key in sorted(all_params.keys())])

        #Obtains the method and the request url
        request_method = request.method
        request_url = request.get_host() + request.path

        SIGNATURE_BASE_STRING = '%s&%s&%s' % (escape(request_method),
                                              escape(request_url),
                                              escape(normalized_string))

        #Calculate the signature. First calculate the base64 digest, then urlescape
        if hauth_signature_method == 'HMAC-SHA1':
            hashed = hmac.new(user_secret, SIGNATURE_BASE_STRING, hashlib.sha1)
            signature = escape(binascii.b2a_base64(hashed.digest())[:-1])
            #Do not include the last character, a newline character, from b2a_base64

        elif hauth_signature_method == 'HMAC-MD5':
            hashed = hmac.new(user_secret, SIGNATURE_BASE_STRING, hashlib.md5)
            signature =  escape(binascii.b2a_base64(hashed.digest())[:-1])
        else:
            #Returns False for an unsupported method
            return False

        if hauth_signature == signature:
            user.last_nonce = hauth_nonce
            user.last_timestamp = hauth_timestamp
            


    def challenge(self):
        return HttpResponseBadRequest

