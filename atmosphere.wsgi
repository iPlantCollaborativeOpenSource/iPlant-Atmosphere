#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


import os
import sys
import site


# developed and tested with wsgi (apache)
# for scalable service, 
# running Djanog with Tornado is not a bad idea at all.


# One directory above the project, so project name will be needed for imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# with mod_wsgi >= 2.4, this line will add this path in front of the python path
#site.addsitedir(os.path.join(root_dir, 'lib/python2.5/site-packages'))
#site.addsitedir('/usr/local/lib/python2.5/site-packages')
site.addsitedir('/opt/atmo_home/VIRTUALENV/lib/python2.6/site-packages')
site.addsitedir('/opt/atmo_home/VIRTUALENV/lib64/python2.6/site-packages')

# add this django project
sys.path.append(root_dir)
print root_dir
#sys.path.append('/opt/atmo_home/atmosphere')
sys.path.append('/opt/atmo_home/VIRTUALENV/lib/python2.6/site-packages')
sys.path.append('/opt/atmo_home/VIRTUALENV/lib64/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'atmosphere.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


os.environ['PYTHON_EGG_CACHE'] = '/opt/atmo_home/atmosphere/cache'
os.environ["CELERY_LOADER"] = "django"
