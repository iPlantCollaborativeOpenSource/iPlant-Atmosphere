#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


from datetime import datetime
from datetime import timedelta

import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

from atmosphere.cloudservice.models import *
from urlparse import urlparse
#from django.utils import simplejson
import json
import atmosphere.cloudservice.api.v1.util as atmo_util

from celery.task import task

import inspect

def get_user_instance_list(userid):
  tasks = Tasks.objects.filter(task_name='get_all_instance_list').order_by('-updated_at')[0]
  task_result = tasks.task_result
  task_result_json = json.loads(task_result)
  task_updated_at = tasks.updated_at
  def is_it(t):
    return t['reservation_owner_id'] == userid
  return filter(is_it,task_result_json)

# for distributed job!

@task
def get_user_instance_list_(all_user_json,userid):
  def is_it(t):
    return t['reservation_owner_id'] == userid
  return filter(is_it,all_user_json)