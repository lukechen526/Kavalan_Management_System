import os, sys
import site

# put virtualenv on pythonpath
site.addsitedir('/opt/webapps/domain.com/lib/python2.6/site-packages')

#add the project directory to PYTHONPATH
path = '/path/to/mysite'
if path not in sys.path:
    sys.path.append(path)

# redirect print statements to apache log
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
  
  