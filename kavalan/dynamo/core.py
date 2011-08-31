#Provides the core functionalities of dynamo
import json
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.db.models import Q

def build_query(queryString, model=None):
    """
    Returns a QuerySet by parsing queryString. Optionally takes 'model', which will override 'app.model' provided by queryString

    :param queryString: the JSON string or dict object to be used for constructing the query
    :param model: *optional* If passed by the caller, the 'app' and 'model' keys in queryString will be ignored
    :return: a QuerySet based on queryString

    """
    
    if not isinstance(queryString, dict):
        #Parse the filter string if it is not already a dict object
        try:
            queryString = json.loads(queryString)
        except ValueError:
            raise ValueError("Cannot parse queryString.")

        except TypeError:
            raise TypeError("queryString must be a dict or JSON string.")

    if not model:
        #if model is not provided, use Content Type to load the model
        if not ('app' in queryString and 'model' in queryString):
            raise KeyError("Keys 'app' and 'model' required")

        try:
            model_type = ContentType.objects.get(app_label=queryString['app'], model=queryString['model'])
            model = model_type.model_class()
        except ContentType.DoesNotExist:
            raise 


    if 'filters' not in queryString:
        raise KeyError("No filters specified")
    elif not isinstance(queryString['filters'], list):
        raise TypeError("'filters' needs to be a list")

    query = Q()

    for f in queryString['filters']:
        #Each filter has four keys:
        #'field': the field for the lookup
        #'lookuptype': the lookup type (e.g. 'lte', 'contains')
        #'value': the value for the lookup
        #'op': the operator to apply with the previous filter (AND or OR)
        #'exclude': determines Q(field__lookuptype=value) or ~Q(field__lookuptype=value)
        #Each filter (a dict obj) gets translated into a Q object

        if not ('field' in f and 'lookuptype' in f and 'value' in f and 'op' in f and 'exclude' in f):
            raise KeyError("Must provide all the keys for filter: 'field','lookuptype', 'value', 'op', and 'exclude' ")

        if  f['field'] not in model._meta.get_all_field_names() and f['field'] not in [ m2m.name for m2m in model._meta._many_to_many()]:
            #Check that the model has f['field'] either as a normal field or a ManyToMany relation
            raise FieldError("The Model does not have this field: %s" % f['field'])

        kwargs = {'%s__%s'%(f['field'], f['lookuptype']): f['value'] }
        q = Q(**kwargs)
        if f['exclude']:
            q = ~q

        if f['op'] == 'AND':
            query.add(q, Q.AND)
        elif f['op'] == 'OR':
            query.add(q, Q.OR)
        else:
            #If no op is provided, defaults to OR
            query.add(q, Q.OR)

    return model._default_manager.filter(query)

            

        

    
    

        


  