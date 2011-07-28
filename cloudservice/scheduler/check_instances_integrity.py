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
import logging



def send_email_to_admin():
  pass

def check_instance_integrity():
  """
    for now current running vms and current pending vms check. 
    for now, only few cases will be caught...

    1) when
        eucalyptus says an instance is not running (not in the euca_describe list) but 
        instances table shows athe instnace is running

    2) when 
        instance's current_running_vms_from_eucalyptus is running 
        and
        instance's current_pending_vms_from_instances_table is pending
        for 180 seconds or more
  """
  #current_running_vms_from_resources_watches = 
  #current_pending_vms_from_resources_watches

  all_instances = json.loads(Resources_watches.objects.raw("SELECT id, resource_get_function_result FROM cloudservice_resources_watches WHERE resource_get_function_name = 'get_all_instances_list' order by updated_at DESC limit 1")[0].resource_get_function_result)
  running_instance = filter(lambda x: x['instance_state'] == "running", all_instances_json)
  running_instance_ids_list = map(lambda x: x['instance_id'], running_instance)

  current_running_vms_from_instances_table = [i.instance_id for i in Instances.objects.filter(current_state = "running")]
  current_pending_vms_from_instances_table = [i.instance_id for i in Instances.objects.filter(current_state = "pending")]
  
  # CASE 1






  # CASE 2








  a = list(set(current_running_vms_from_eucalyptus) & set(current_pending_vms_from_instances_table))
  # last 180 sec of a 
