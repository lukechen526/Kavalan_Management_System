# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User, Group

class DocumentEngineTest(TestCase):
    
    fixtures = ['docs.json']

    def setUp(self):

        test_user = User.objects.create_user(username='test', email='test@example.com', password='test')
        test_group = Group.objects.create(name='Test Group')

    def testAuthenticationRequired(self):
        resp = self.client.get('/doc_engine/')
        self.assertRedirects(resp, '/accounts/login/?next=/doc_engine/' )

    def testAPIAuthenticationRequired(self):
        resp = self.client.get('/api/documents/')
        self.assertEqual(resp.status_code, 401) #Forbidden for anonyous client

    def testPageExist(self):
        c = self.client
        c.login(username='test', password='test')
        resp = c.get('/doc_engine/')
        self.assertContains(resp, 'Search Documents')
        self.assertContains(resp, 'Search Batch Records')

    def testDocumentQuery(self):
        c = self.client
        c.login(username='test', password='test')
        query = '{"sn_title":"he","document_level":"","labels":null}'
        page_number = 1
        resp = c.get('/api/documents/', {'query': query, 'page_number': page_number})
        self.assertContains(resp, '"title": "HEllo world"')

    def testBatchRecordQuery(self):
        c = self.client
        c.login(username='test', password='test')
        query = '{"name":"amp","batch_number":"","date_manufactured_from":"2011-02-01","date_manufactured_to":""}'
        resp = c.get('/api/batchrecords/', {'query': query, 'page_number': 1})
        
        self.assertContains(resp, 'objects')
        



        

    