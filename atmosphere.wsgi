#
# Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
# This software is licensed under the CC-GNU GPL version 2.0 or later.
# License: http://creativecommons.org/licenses/GPL/2.0/
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

import os
import sys
import site

# One directory above the project, so project name will be needed for imports
#root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# with mod_wsgi >= 2.4, this line will add this path in front of the python path
#site.addsitedir(os.path.join(root_dir, 'lib/python2.5/site-packages'))
site.addsitedir('/usr/local/lib/python2.5/site-packages')

# add this django project
#sys.path.append(root_dir)
sys.path.append('/home/atmosphere_dev/')
#sys.path.append('/home/atmosphere_preview_101020/atmosphere')
sys.path.append('/usr/local/lib/python2.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'atmosphere.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
