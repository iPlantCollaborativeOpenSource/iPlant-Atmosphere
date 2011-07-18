#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from celery.decorators import task
#from celery.task.schedules import crontab #DeprecationWarning: celery.task.schedules is deprecated and renamed to celery.schedules  "celery.task.schedules is deprecated and renamed to celery.schedules"))
from celery.schedules import crontab
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

from atmosphere.cloudservice.scheduler.get_all_instances_list import get_all_instances_list as run_get_all_instances_list
from atmosphere.cloudservice.scheduler.terminate_scheduled_instances import terminate_scheduled_instances as run_terminate_scheduled_instances
#from atmosphere.cloudservice.scheduler.terminate_scheduled_instances import send_termination_notification_mail
from atmosphere.cloudservice.scheduler.send_termination_notification_mail import send_termination_notification_mail
from atmosphere.cloudservice.scheduler.get_all_images_list import get_all_images_list as run_get_all_images_list
from atmosphere.cloudservice.scheduler.launch_instances import launch_instances as run_launch_instances

def write_log(msg):
  file = open("/home/atmosphere_dev/atmosphere/logs/scheduler.log","a")
  a = datetime.now()
  stmt = a.strftime("%A, %d. %B %Y %I:%M%p %S") + " >>> " + msg
  file.write(stmt+"\n") 

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  
#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
#def hello_world():
#  write_log("hello_world")

#CENTRAL INIT SCHEDULE - RUNS EVERY 20 SECONDS
@periodic_task(run_every=timedelta(seconds=20))
def base_schduler():
  run_get_all_images_list()

@periodic_task(run_every=timedelta(seconds=20))
def get_all_instances_list():
  run_get_all_instances_list()

@periodic_task(run_every=timedelta(seconds=30))
def terminate_scheduled_instance():
  run_terminate_scheduled_instances()

@periodic_task(run_every=timedelta(seconds=10))
def launch_instances():
  if len(Configs.objects.filter(key="_launch_instances_lock")[:1]) == 0 :
    Configs(key = "_launch_instances_lock", value = "False").save()
    run_launch_instances()
  else : 
    config = Configs.objects.filter(key="_launch_instances_lock")[:1][0]
    if config.value == 'False':
      config.value = 'True'
      config.save()
      if run_launch_instances(): 
        config.value = 'False'
        config.save()
    else :
      pass
      

#@periodic_task(run_every=timedelta(seconds=10))
#def launch_instances():
#  run_launch_instances()


#@periodic_task(run_every=timedelta(seconds=20))
#def get_all_images_list():
#  run_get_all_images_list()

