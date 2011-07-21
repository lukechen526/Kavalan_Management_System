from hermes.api import *
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
import json
from django.utils.http import urlquote_plus
import hashlib, hmac
import binascii

def escape(s):
    return urlquote_plus(s, safe='~')

def create_signature(request_method, request_path, hauth_key, hauth_secret, hauth_timestamp, hauth_nonce,
                     hauth_signature_method='HMAC-SHA1', kwarg_a='', kwarg_b=''):


    normalized_string = '&'.join([
        'hauth_key=' + escape(hauth_key),
        'hauth_nonce=' + escape(hauth_nonce),
        'hauth_signature_method=' + escape(hauth_signature_method),
        'hauth_timestamp=' + escape(hauth_timestamp),
        'kwarg_a=' + escape(kwarg_a),
        'kwarg_b=' + escape(kwarg_b)
    ])

    SIGNATURE_BASE_STRING = '&'.join([escape(request_method),
                                      escape(request_path),
                                      escape(normalized_string)
                                      ])

    if hauth_signature_method == 'HMAC-SHA1':
        hashed = hmac.new(hauth_key, SIGNATURE_BASE_STRING, hashlib.sha1)
    else:
        hashed = hmac.new(hauth_key, SIGNATURE_BASE_STRING, hashlib.md5)

    return escape(binascii.b2a_base64(hashed.digest())[:-1])



class HermesAPITestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')


    def test_request_key_secret_pair_fail(self):
        resp = self.client.post('/api/hermes/request_key_secret_pair')
        self.assertEqual(resp.status_code, 401)

    def test_request_key_secret_pair_success(self):

        self.client.login(username='test', password='test')
        resp = self.client.post('/api/hermes/request_key_secret_pair')
        self.assertEqual(resp.status_code, 200)

    def test_hauth_authentication(self):

        #Get a key/secret pair
        self.client.login(username='test', password='test')
        resp = self.client.post('/api/hermes/request_key_secret_pair')
        pair = json.loads(resp.content)
        key = pair['key']
        secret = pair['secret']

        #Setup a valid request
        request_method = 'POST'
        request_path = 'http://localhost:8000/api/hermes/test_authentication'
        HTTP_AUTHORIZATION = '''HAuth
        hauth_key="%s",
        



        '''




    