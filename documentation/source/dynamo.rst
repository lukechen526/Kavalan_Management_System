.. _dynamo:

Dynamo
=======

Overview
---------------
**Dynamo** is the sub-system that adds the functionality of dynamic filtering based on user input to any model.
e.g. a dictionary-object::

    {'app': 'doc_engine',
    'model':'Document',
    'filters':[{'field': 'title', 'lookuptype':'contains', 'value':'AF', 'op':'', 'exclude':False }]}



gets translated into::

    Document.objects.filter(Q(title__contains='AF'))

Dynamo does all the necessary validation on the user input to ensure that the fields to which the filters are applied
actually exist.

