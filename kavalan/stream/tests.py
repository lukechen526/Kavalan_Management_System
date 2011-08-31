from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test.client import Client
import json


class StreamAPITest(TestCase):

    def setUp(self):
        #Creates a test group
        self.test_group_1 = Group.objects.create(name='Test Group 1')
        self.group_id_1 = self.test_group_1.id
        
        #Creates two test users of test_group_1
        test = User.objects.create_user(username='test', password='test')
        test.groups.add(self.test_group_1)
        test.save()

        test2 = User.objects.create_user(username='test2', password='test2')
        test2.groups.add(self.test_group_1)
        test2.save()

    def test_post_to_stream_success(self):
        c = Client(enforce_csrf_checks=True)
        c.login(username='test', password='test')
        
        model = {'groups':[self.group_id_1],
                 'content': 'Hello World!',
                 'link': 'http://www.google.com'
                 }

        resp = c.post('/api/stream/', {'model': json.dumps(model)})
        print resp.content
        self.assertEqual(resp.status_code, 200)

    def test_post_to_stream_bad_group(self):
        self.client.login(username='test', password='test')
        model = {'groups':[self.group_id_1+1],
                 'content': 'Hello World!',
                 'link': 'http://www.google.com'
                 }

        resp = self.client.post('/api/stream/', {'model': json.dumps(model)})
        print resp.content
        self.assertNotEqual(resp.status_code, 200)

    def test_no_empty_content_link(self):
        self.client.login(username='test', password='test')
        model = {'groups':[self.group_id_1],
                 'content': '',
                 'link': ''
                 }
        resp = self.client.post('/api/stream/', {'model': json.dumps(model)})
        print resp.content
        self.assertEqual(resp.status_code, 400)

    def test_update_success(self):
        c = Client(enforce_csrf_checks=True)
        c.login(username='test', password='test')

        model = {'groups':[self.group_id_1],
                 'content': 'Hello World!',
                 'link': ''
                 }

        resp = c.post('/api/stream/', {'model': json.dumps(model)})
        print resp.content
        post_id = json.loads(resp.content)['id']
        model['content'] = 'UPDATED!'
        model['link'] = 'http://www.yahoo.com'
        resp = c.put('/api/stream/%s' % (post_id,), {'model': json.dumps(model)})
        print resp.content
        self.assertEqual(resp.status_code, 200)

    def test_update_not_original_poster(self):
        c = Client(enforce_csrf_checks=True)
        c.login(username='test', password='test')

        model = {'groups':[self.group_id_1],
                 'content': 'Hello World!',
                 'link': 'http://www.google.com'
                 }

        resp = c.post('/api/stream/', {'model': json.dumps(model)})
        post_id = json.loads(resp.content)['id']

        #Changes user to test2
        c.logout()
        c.login(username='test2', password='test2')
        model['content'] = 'UPDATED!'
        resp = c.put('/api/stream/%s' % (post_id,), {'model': json.dumps(model)})
        print resp.content
        self.assertEqual(resp.status_code, 401)

    def test_delete_success(self):
        c = Client(enforce_csrf_checks=True)
        c.login(username='test', password='test')

        model = {'groups':[self.group_id_1],
                 'content': 'Hello World!',
                 'link': 'http://www.google.com'
                 }

        resp = c.post('/api/stream/', {'model': json.dumps(model)})
        post_id = json.loads(resp.content)['id']

        #Delete the post
        resp = c.delete('/api/stream/%s' %(post_id,))
        self.assertEqual(resp.status_code, 204) #Status code: DELETED

    def test_delete_nonexistent_id(self):
        c = Client(enforce_csrf_checks=True)
        c.login(username='test', password='test')

        model = {'groups':[self.group_id_1],
                 'content': 'Hello World!',
                 'link': 'http://www.google.com'
                 }

        resp = c.post('/api/stream/', {'model': json.dumps(model)})
        post_id = json.loads(resp.content)['id'] + 1

        #Try deleting the post; should fail because of invalid post_id
        resp = c.delete('/api/stream/%s' %(post_id,))
        print resp.content
        self.assertNotEqual(resp.status_code, 204) #Status code: DELETED

        










        
