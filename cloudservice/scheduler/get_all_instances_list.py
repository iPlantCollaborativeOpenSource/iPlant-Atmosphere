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

import inspect

def get_all_instances_list():
  ec2_key = Configs.objects.get(key = "admin_ec2_access_key").value
  ec2_secret = Configs.objects.get(key = "admin_ec2_secret_key").value
  ec2_url = Configs.objects.get(key = "admin_ec2_url").value
  region = RegionInfo(name="eucalyptus", endpoint=urlparse(ec2_url).netloc.split(":")[0])
  connection = boto.connect_ec2(aws_access_key_id=str(ec2_key),
  								aws_secret_access_key=str(ec2_secret),
                              	is_secure=False,
                              	region=region,
                              	port=8773,
                              	path="/services/Eucalyptus")
  reservations = connection.get_all_instances()
  instance_ids = ""
  instance_num = 0
  instance_json_string = ""
  for reservation in reservations:
    reservation_string = '%s\t%s' % (reservation.id, reservation.owner_id)
    group_delim = '\t'
    for group in reservation.groups:
      reservation_string += '%s%s' % (group_delim, group.id)
      group_delim = ', '
      #print 'RESERVATION\t%s' % (reservation_string)
    instances = []
    for instance in reservation.instances:
      if instance.id in instance_ids:
        instances.append(instance)
      else:
        instances = reservation.instances
    for instance in instances:
      instance_num = instance_num + 1
      try :
        instance_name = Instances.objects.get(instance_id = instance.id).instance_name
      except :
        instance_name = ""
      try :
        instance_description = Instances.objects.get(instance_id = instance.id).instance_description
      except :
        instance_description = ""
      try :
        instance_tags = Instances.objects.get(instance_id = instance.id).instance_tags
      except :
        instance_tags = ""
      if instance:
        instance_image_name = ""
        try :
          instance_image_name = Machine_images.objects.get(image_id = instance.image_id).image_name
        except :
          instasnce_image_name = ""
        instance_json_string = instance_json_string + """
        {
              "instance_num" : "%s" ,
              "instance_name" : "%s" ,
              "instance_description" : "%s",
              "instance_tags" : "%s",
              "reservation_id" : "%s" ,
              "reservation_owner_id" : "%s" ,
              "group_id" : "%s" ,
              "instance_id" : "%s" ,
              "instance_image_id": "%s" ,
              "instance_image_name" : "%s" , 
              "instance_public_dns_name" : "%s" ,
              "instance_private_dns_name" : "%s" ,
              "instance_state" : "%s" ,
              "instance_key_name" : "%s" ,
              "instance_ami_launch_index" : "%s" ,
              "instance_product_codes" : "%s" ,
              "instance_instance_type" : "%s" ,
              "instance_launch_time" : "%s" ,
              "instance_placement" : "%s" ,
              "instance_kernel" : "%s" ,
              "instance_ramdisk" : "%s"
         }, """ % (
              instance_num ,
              instance_name ,
              instance_description.replace("\n", "<br>"),
              instance_tags , 
              reservation.id,
              reservation.owner_id ,
              group.id,
              instance.id,
              instance.image_id,
              instance_image_name,
              instance.public_dns_name,
              instance.private_dns_name,
              instance.state,
              instance.key_name,
              instance.ami_launch_index,
              instance.product_codes ,
              instance.instance_type,
              instance.launch_time,
              instance.placement,
              instance.kernel,
              instance.ramdisk
            )
      return_json_str = "[%s]" % instance_json_string[0:-2]
  #Monitor_instance_list
  tasks = Tasks(task_name=inspect.stack()[0][3],task_result=''.join(return_json_str.splitlines()).replace('  ',''))
  tasks.save()