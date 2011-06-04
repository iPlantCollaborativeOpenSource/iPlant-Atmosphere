#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from celery.decorators import task
from celery.task.schedules import crontab 
from celery.decorators import periodic_task  


from datetime import datetime
from datetime import timedelta


import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo


from atmosphere.cloudservice.models import *
from urlparse import urlparse
from django.utils import simplejson
import atmosphere.cloudservice.api.v1.util as atmo_util

import inspect

from atmosphere.cloudservice.task.get_all_instance_list import get_all_instance_list as run_get_all_instance_list

def write_log(msg):
  file = open("/home/atmosphere_dev/atmosphere/logs/scheduler.log","a")
  a = datetime.now()
  stmt = a.strftime("%A, %d. %B %Y %I:%M%p %S") + " >>> " + msg
  file.write(stmt+"\n") 

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def hello_world():
  write_log("hello_world")

@periodic_task(run_every=timedelta(seconds=20))
def get_all_instance_list():
  run_get_all_instance_list()
