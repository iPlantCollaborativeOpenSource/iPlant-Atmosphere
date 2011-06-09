#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from atmosphere.cloudservice.models import *
import json


from celery.task import task


@task
def get_current_instance_status(all_instance_info_json):
  all_instances_list = Tasks.objects.filter(task_name = 'get_all_instances_list').order_by('-updated_at')[0].task_result
  ail = json.loads(all_instances_list)
  #ail = json.loads(all_instance_info_json)
  total_number_of_vms = len(ail)
  number_of_running_instance = len(filter(lambda e : e['instance_state'] == 'running',ail))
  number_of_pending_instance = len(filter(lambda e : e['instance_state'] == 'pending',ail))
  number_of_shutting_down_instance = len(filter(lambda e : e['instance_state'] == 'shutting-down',ail))
  return "%s %s %s %s" % (total_number_of_vms, number_of_running_instance, number_of_pending_instance, number_of_shutting_down_instance)
