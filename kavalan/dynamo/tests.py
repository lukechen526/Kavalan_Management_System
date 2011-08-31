from django.core.exceptions import FieldError
from django.test import TestCase
from dynamo import core
from django.db import models
from doc_engine.models import Document

class BuildQueryTestCase(TestCase):

    fixtures = ['docs.json']

    def testDict(self):
        d_dict  = {'app': 'doc_engine',
                   'model':'Document',
                   'filters':[{'field': 'serial_number', 'lookuptype':'contains', 'value':'AF', 'op':'', 'exclude':False }]}
        result = core.build_query(d_dict)
        self.assertIsInstance(result, models.query.QuerySet)
        #There should be at least one result
        self.assertTrue(result)

    def testJSON(self):
        d_json = '{"app": "doc_engine", "model": "Document", "filters": [{"lookuptype": "contains", "field": "serial_number", "exclude": false, "value": "AF", "op": ""}]}'
        result = core.build_query(d_json)
        self.assertIsInstance(result, models.query.QuerySet)
        #There should be at least one result
        self.assertTrue(result)


    def testWithModel(self):
        d_with_model = '{"filters": [{"lookuptype": "contains", "field": "serial_number", "exclude": false, "value": "AF", "op": ""}]}'
        result = core.build_query(d_with_model, Document)
        self.assertIsInstance(result, models.query.QuerySet)
        #There should be at least one result
        self.assertTrue(result)

    def testNoResult(self):
        d_json = '{"app": "doc_engine", "model": "Document", "filters": [{"lookuptype": "contains", "field": "title", "exclude": false, "value": "XXXXXXXXXXXXXXX", "op": ""}]}'
        result = core.build_query(d_json)
        self.assertFalse(result)
        #the returned QuerySet should be empty

    def testFieldError(self):
        d_attribute_error = '{"app": "doc_engine", "model": "Document", "filters": [{"lookuptype": "contains", "field": "sex", "exclude": false, "value": "XXXXXXXXXXXXXXX", "op": ""}]}'
        self.assertRaises(FieldError, core.build_query, d_attribute_error)
        
    def testTypeError(self):
        d_type_error = []
        self.assertRaises(TypeError, core.build_query, d_type_error)

    def testValueError(self):
        d_value_error = "{'app': 'doc_engine', 'filters':[{'field': 'title','value':'AF', 'op':'', 'exclude':'False' }]}"
        self.assertRaises(ValueError, core.build_query, d_value_error)


        




