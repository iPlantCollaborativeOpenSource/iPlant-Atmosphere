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
  #all_instances_list = Tasks.objects.filter(task_name = 'get_all_instances_list').order_by('-updated_at')[0].task_result
  #ail = json.loads(all_instances_list)
  ail = json.loads(all_instance_info_json)
  total_number_of_vms = len(ail)
  number_of_running_instance = len(filter(lambda e : e['instance_state'] == 'running',ail))
  number_of_running_m1_small = len(filter(lambda f : f['instance_instance_type'] == 'm1.small', filter(lambda e : e['instance_state'] == 'running',ail)))
  number_of_running_c1_medium = len(filter(lambda f : f['instance_instance_type'] == 'c1.medium', filter(lambda e : e['instance_state'] == 'running',ail)))
  number_of_running_m1_large = len(filter(lambda f : f['instance_instance_type'] == 'm1.large', filter(lambda e : e['instance_state'] == 'running',ail)))
  number_of_running_m1_xlarge = len(filter(lambda f : f['instance_instance_type'] == 'm1.xlarge', filter(lambda e : e['instance_state'] == 'running',ail)))
  number_of_running_c1_xlarge = len(filter(lambda f : f['instance_instance_type'] == 'c1.xlarge', filter(lambda e : e['instance_state'] == 'running',ail)))
  number_of_pending_instance = len(filter(lambda e : e['instance_state'] == 'pending',ail))
  number_of_shutting_down_instance = len(filter(lambda e : e['instance_state'] == 'shutting-down',ail))
  return_json = """[{"number_of_running_m1_small" : %i}, {"number_of_running_c1_medium" : %i}, {"number_of_running_m1_large" : %i}, {"number_of_running_m1_xlarge" : %i}, {"number_of_running_c1_xlarge" : %i }, {"number_of_pending_instance" : %i}, {"number_of_shutting_down_instance" : %i}]""" %
    (number_of_running_m1_small,number_of_running_c1_medium,number_of_running_m1_large,number_of_running_m1_xlarge,number_of_running_c1_xlarge,number_of_pending_instance,number_of_shutting_down_instance)
  return return_json
