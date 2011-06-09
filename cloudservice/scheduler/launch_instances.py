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
from django.utils import simplejson
import atmosphere.cloudservice.api.v1.util as atmo_util

from datetime import timedelta

import inspect
import json


def current_vms_launching_status():
  """
    I dont use this function. 
    see "get_current_instance_status.py" in task module
  """
  all_instances_list = Tasks.objects.filter(task_name = 'get_all_instances_list').order_by('-updated_at')[0].task_result
  ail = json.loads(all_instances_list)
  total_number_of_vms = len(ail)
  number_of_running_instance = len(filter(lambda e : e['instance_state'] == 'running',ail))
  number_of_pending_instance = len(filter(lambda e : e['instance_state'] == 'pending',ail))
  number_of_shutting_down_instance = len(filter(lambda e : e['instance_state'] == 'shutting-down',ail))
  return "%s %s %s %s" % (total_number_of_vms, number_of_running_instance, number_of_pending_instance, number_of_shutting_down_instance)

def launch_instances():

  pass