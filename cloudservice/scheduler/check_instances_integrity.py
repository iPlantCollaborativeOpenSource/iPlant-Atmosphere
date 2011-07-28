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

from django.core.mail import send_mail


def send_email_to_admin(subject=None, message=None):
  admin_email = Configs.objects.get(key="admin_email").value
  if subject == None :
    subject = "cloud admin email from atmosphere"
  send_mail(subject, message, admin_email, [admin_email], fail_silently=False)

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

  all_instances = json.loads(Resources_watches.objects.raw("SELECT id, resource_get_function_result FROM cloudservice_resources_watches WHERE resource_get_function_name = 'get_all_instances_list' order by updated_at DESC limit 1")[0].resource_get_function_result)
  running_instance = filter(lambda x: x['instance_state'] == "running", all_instances)
  running_instance_ids_list = map(lambda x: x['instance_id'], running_instance)
  pending_instance = filter(lambda x: x['instance_state'] == "pending", all_instances)
  pending_instance_ids_list = map(lambda x: x['instance_id'], pending_instance)
  running_pending_instance_ids_list = running_instance_ids_list + pending_instance_ids_list

  current_running_vms_from_instances_table = [i.instance_id for i in Instances.objects.filter(current_state = "running")]
  current_pending_vms_from_instances_table = [i.instance_id for i in Instances.objects.filter(current_state = "pending")]
  current_running_pending_vms_from_instances_table = current_running_vms_from_instances_table + current_pending_vms_from_instances_table
  
  # CASE 1: Missing instances
  #set(current_running_vms_from_instances_table)
  #set(running_instance_ids_list)

  if len(current_running_pending_vms_from_instances_table) > 0 :
    if not set(current_running_pending_vms_from_instances_table).issubset(set(running_pending_instance_ids_list)) :
      lost_instnace_list = ", ".join(list(set(current_running_pending_vms_from_instances_table) - set(running_pending_instance_ids_list)))

      for i in list(set(current_running_pending_vms_from_instances_table) - set(running_pending_instance_ids_list)):
        instances = Instances.objects.get(instance_id = i)
        instances.current_state = "lost"
        instances.save()

      message = "Atmosphere detects following instances are lost:\n"+lost_instnace_list
      send_email_to_admin(subject="Lost instance alert",message=message)
      # do i need to update database ??? - I don't know.. ummmm

  # CASE 2: Failed instances











