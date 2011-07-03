#Provides the core functionalities of dynamo
import json
from django.contrib.contenttypes.models import ContentType
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
            raise

    if not model:
        #if model is not provided, use Content Type to load the model
        if not ('app' in queryString and 'model' in queryString):
            raise KeyError("Keys 'app' and 'model' required")

        model_type = ContentType.objects.get(app_label=queryString['app'], model=queryString['model'])
        model = model_type.model_class()

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

            

        

    
    

        


  