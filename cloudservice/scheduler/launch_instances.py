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
from datetime import datetime

import inspect
import json
import logging

def current_vms_launching_status():
  """
    I don't use this function. 
    see "get_current_instance_status.py" in task module
  """
  all_instances_list = Resources_watches.objects.filter(resource_get_function_name = 'get_all_instances_list').order_by('-updated_at')[0].resource_get_function_result
  ail = json.loads(all_instances_list)
  total_number_of_vms = len(ail)
  number_of_running_instance = len(filter(lambda e : e['instance_state'] == 'running',ail))
  number_of_pending_instance = len(filter(lambda e : e['instance_state'] == 'pending',ail))
  number_of_shutting_down_instance = len(filter(lambda e : e['instance_state'] == 'shutting-down',ail))
  return """{ "total_number_of_vms" : "%s", "number_of_running_instance" : "%s", "number_of_pending_instance" : "%s", "number_of_shutting_down_instance" : "%s" }""" % (total_number_of_vms, number_of_running_instance, number_of_pending_instance, number_of_shutting_down_instance)

def current_vm_status_from_cloudservice_instances():
  # select distinct(current_state) from cloudservice_instances
  # Instances.objects.all().values('current_state').distinct()
  # Instances.objects.all().values_list('current_state',flat=True).distinct()
  a = ""
  for state in Instances.objects.all().values_list('current_state',flat=True).distinct() :
    a = a + "\"state_%s\": %s, " % (state, str(len(Instances.objects.filter(current_state = state))))
  return "{"+a[:-2]+"}"

def current_vm_status_from_boto():
  pass

def match():
  pass

def launch_instances():
  #logging.error("lunach instances called")
  concurrent_launchable_instance_num = Configs.objects.get(key="concurrent_launchable_instance_num").value 
  
  k = int(concurrent_launchable_instance_num) - int(json.loads(current_vms_launching_status())['number_of_pending_instance'])
  #logging.error(str(k))

  #if k == 0 :
  #  logging.error("zero que")
  #else :
  #  logging.error("que:"+str(concurrent_launchable_instance_num))

  #if int(json.loads(current_vms_launching_status())['number_of_pending_instance']) < concurrent_launchable_instance_num :
  if k > 0 :    
    #instances = Instances.objects.filter(current_state = "qued").order_by('-launch_request_time')[:concurrent_launchable_instance_num]
    instances = Instances.objects.filter(current_state = "qued").order_by('launch_request_time')[:k]
    current_time = datetime.now()
    #loop 
    for instance in instances:
      owner = instance.owner_id
      ec2_key = Ec2_keys.objects.get(username = owner).ec2_access_key 
      ec2_secret = Ec2_keys.objects.get(username = owner).ec2_secret_key 
      ec2_url = Ec2_keys.objects.get(username = owner).ec2_url
      #user_data = Machine_image_userdata_scripts.objects.get(script_id=(User_applications.objects.get(application_id = user_app_id)).machine_image_user_data_scripts_script_id).script

      region = RegionInfo(name="eucalyptus", endpoint=urlparse(ec2_url).netloc.split(":")[0])
      connection = boto.connect_ec2(aws_access_key_id=str(ec2_key), aws_secret_access_key=str(ec2_secret), is_secure=False, region=region, port=8773, path="/services/Eucalyptus")
      #connection.run_instance(machine_image,min_count=1,max_count=1)
      #run_instances(image_id, min_count=1, max_count=1, key_name=None, security_groups=None, user_data=None, addressing_type=None, instance_type='m1.small', placement=None, kernel_id=None, ramdisk_id=None, monitoring_enabled=False, subnet_id=None, block_device_map=None)

      reservation = connection.run_instances(image_id=instance.machine_image,min_count=1,max_count=1,key_name=instance.key_name, 
        user_data=instance.user_data,
        instance_type=instance.machine_size
      )
      #ami_launch_index
      #block_device_mapping
      #confirm_product
      #connection
      #dns_name
      #endElement
      #get_console_output
      #instance_id = reservation.instances[0].id
      #image_id
      #instanceState
      #instance_class
      #instance_type
      #ip_address
      #item
      #kernel
      #key_name
      #launch_time
      #monitor
      #monitored
      #monitoring
      #persistent
      #placement
      #previous_state
      #private_dns_name
      #private_ip_address
      #product_codes
      #public_dns_name
      #ramdisk, 
      #reason
      #reboot, 
      #region, 
      #requester_id', 
      #root_device_name
      #shutdown_state
      #spot_instance_request_id', 'startElement', 'state', 'state_code', 'stop', 'subnet_id', 'unmonitor', 'update', 'use_ip', 'vpc_id']
      instance.instance_id = reservation.instances[0].id
      instance.current_state = reservation.instances[0].state
      #instance.reservation =
      #instance.group_id = 
      instance.public_dns_name = reservation.instances[0].public_dns_name
      instance.private_dns_name = reservation.instances[0].private_dns_name
      instance.key_name = reservation.instances[0].key_name
      instance.ami_index = reservation.instances[0].ami_launch_index
      #instance.product_code
      instance.launch_time = reservation.instances[0].launch_time
      instance.launch_request_run_time = current_time
      instance.placement = reservation.instances[0].region #<== this only returns "RegionInfo:eucalyptus" this should be zone name
      instance.kernel = reservation.instances[0].kernel
      instance.ramdisk = reservation.instances[0].ramdisk

      instance.save()

      # this should be unnecessary if we track with atmosphere_resource_id but now we track with instance_id. should be changed later
      instance_lifecycle = Instance_lifecycles.objects.get(atmosphere_resource_id = instance.atmosphere_resource_id)
      instance_lifecycle.instance_id = reservation.instances[0].id
      instance_lifecycle.instance_launched_at = current_time
      instance_lifecycle.save()
  return True