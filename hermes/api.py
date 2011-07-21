from piston.handler import BaseHandler
from piston.utils import *
from hermes.models import MessageThread, Message, ThreadParticipation, ThreadOwnership, UserHAuthParameters
from django.conf import settings
from django.http import HttpResponseBadRequest, QueryDict
import random
import string
import hmac, hashlib
from urllib import quote_plus, unquote
import binascii

#WARNING!
#It is expected that all request will be conducted via https

#Utility functions
def escape(s):
    return quote_plus(s, safe='~')

class RequestKeySecretPairHandler(BaseHandler):
    """
    The handler used to generate a key/secret pair. Limited to authenticated users only.
    """
    allowed_methods = ('POST',)
    model = UserHAuthParameters
    fields = ('key', 'secret')

    def create(self, request):
        user = request.user
        key, secret = self.generate_key_secret_pair()
        user_params, created = UserHAuthParameters.objects.get_or_create(user=user)
        user_params.key, user_params.secret = key, secret
        user_params.save()
        return user_params
    
    def generate_key_secret_pair(self, length=30):
        """
        Generates a random key/secret key pair in the form of two alphanumeric strings of the specified length
        :param length: length of the string to be generated. Default = 30
        :return: a tuple of (key, secret)
        """
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
        secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
        return key, secret


class HAuthenticationHandler(object):
    """
    Implements a OAuth-like, but more lightweight protocol for authentication/authorization in Hermes.
    The client will request the key/secret pair from the server directly. The key/secret pair then allows the client to
    sign its requests and pass it to a third-party (e.g. a Node.js+Socket.io server) for delivery.
    """
    def is_authenticated(self, request):
        #Validates that the request has all the necessary HAuth parameters and
        #
        if not HAuthenticationHandler.is_valid_request(request):
            return False
        
        #Verifies the signature
        if not HAuthenticationHandler.verify_signature(request):
            return False

    @staticmethod
    def is_valid_request(request):

        must_have = [ 'hauth_' + s for s in ['key', 'signature', 'timestamp', 'nonce', 'signature_method']]
        is_in = lambda l: all([ (p in l) for p in must_have ])
        auth_params = request.META.get('HTTP_AUTHORIZATION', '')
        req_params = request.REQUEST
             
        if not is_in(auth_params) and  not is_in(req_params):
            return False

        #Checks the timestamp and the nonce

    @staticmethod
    def _split_header(header):
        """Turn Authorization: header into parameters."""
        params = {}
        parts = header.split(',')
        for param in parts:
            # Ignore realm parameter.
            if param.find('realm') > -1:
                continue
            # Remove whitespace.
            param = param.strip()
            # Split key-value.
            param_parts = param.split('=', 1)
            # Remove quotes and unescape the value.
            params[param_parts[0]] = unquote(param_parts[1].strip('\"'))
        return params

    @staticmethod
    def verify_signature(request):
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
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header[:6] == 'HAuth ':
            auth_header = auth_header[6:]
            try:
                # Get the parameters from the header.
                auth_params = HAuthenticationHandler._split_header(auth_header)
            except:
                #If any exception was encountered
                auth_params = dict()

        req_params = request.REQUEST
        all_params = req_params.copy()
        all_params.update(auth_params)
        all_params = all_params.dict()

        hauth_signature = all_params.pop('hauth_signature')
        hauth_signature_method = all_params.get('hauth_signature_method')

        user_key = all_params.get('hauth_key')
        
        #Tries retrieving the secret
        try:
            user_params = UserHAuthParameters.objects.get(key=user_key)
            user_secret = escape(user_params.secret)
        except UserHAuthParameters.DoesNotExist:
            return False

        #Verifies that the timestamp and nonce are value before checking the signature
        hauth_timestamp = all_params['hauth_timestamp']
        hauth_nonce = all_params['hauth_nonce']

        #Verifies that the timestamp used for this request is at least as recent as the last used one
        if int(hauth_timestamp) < int(user_params.last_timestamp):
            return False
        #Verifies that the nonce is unique for this timestamp. EACH request using the same timestamp needs a unique
        #nonce
        if user_params.check_duplicate_nonce(hauth_nonce):
            return False

        #Checks if the calculated signature is identical to the one sent in the request
        #Sorts the keys of all_params and generate the string with normalized request parameters. All parameters
        #need to be encoded in UTF-8 first, the URL-escaped.
        
        normalized_string = '&'.join(['%s=%s' % (escape(key.encode('utf-8')),escape(all_params[key].encode('utf-8')))
                                      for key in sorted(all_params.keys()) ])

        #Obtains the method and the request url
        request_method = request.method
        request_url = request.build_absolute_uri(request.path)

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
            if hauth_timestamp != user_params.last_timestamp:
                user_params.last_timestamp = hauth_timestamp
                user_params.clear_all_nonces()
                user_params.add_nonce(hauth_nonce)
            else:
                user_params.add_nonce(hauth_nonce)
            user_params.save()
            return True
        
        else:
            return False

    def challenge(self):
        return rc.FORBIDDEN


class TestAuthenticationHandler(BaseHandler):
    """
    Returns an empty response with code 200. Used to test HAuthenticationHandler
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = UserHAuthParameters
    fields = ('user',('username',))

    def read(self):
        return rc.ALL_OK
    def create(self):
        return rc.ALL_OK
    def update(self):
        return rc.ALL_OK
    def delete(self):
        return rc.ALL_OK
