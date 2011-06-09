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

def get_all_images_list():
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
  images = connection.get_all_images()
  image_json_string = ""
  for image in images :
    if image.type == "machine" :
    # get atmosphere info
      try :
        image_name = Machine_images.objects.filter(image_id = image.id).order_by('-id')[0].image_name
      except :
        image_name = ""
      try :
        image_description = Machine_images.objects.filter(image_id = image.id).order_by('-id')[0].image_description
        if image_description == None :
          image_descriontino = ""
      except :
        image_description = ""
      try :
        image_tags = Machine_images.objects.filter(image_id = image.id).order_by('-id')[0].image_tags
        if image_tags == None :
          image_tags = ""
      except :
        image_tags = "no tags"
      try : 
        image_condition = Machine_images.objects.filter(image_id = image.id).order_by('-id')[0].image_condition
      except :
        image_condition = ""
        #image.id, image.location, image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id
        if image.is_public:
          image.is_public = "public"
        else :
          image.is_public = "private"
      try : 
        image_type = Machine_images.objects.filter(image_id = image.id).order_by('-id')[0].image_type
      except :
        image_type = ""
      image_description = image_description.replace("\n", "<br>") if image_description != None else ""
      image_json_string = image_json_string +"""{ "image_name" : "%s", 
        "image_description" : "%s", 
        "image_tags" : "%s", 
        "image_id" : "%s" , 
        "image_location" : "%s" , 
        "image_ownerid" : "%s" , 
        "image_state" : "%s" ,
        "image_is_public" : "%s" ,
        "image_product_codes" : "%s" ,
        "image_architecture" : "%s" ,"image_type" : "%s","image_ramdisk_id" : "%s","image_kernel_id" : "%s", "image_condition" : "%s" }, """ % (
        image_name,
        image_description,
        image_tags,
        image.id,
        image.location,
        image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id, image_condition
      )
  return_json_str = "[%s]" % image_json_string[0:-2]
  tasks = Tasks(task_name=inspect.stack()[0][3],task_result=''.join(return_json_str.splitlines()).replace('  ',''))
  tasks.save()


#  instance_json_string = ""
#  for reservation in reservations:
#    reservation_string = '%s\t%s' % (reservation.id, reservation.owner_id)
#    group_delim = '\t'
#    for group in reservation.groups:
#      reservation_string += '%s%s' % (group_delim, group.id)
#      group_delim = ', '
#      #print 'RESERVATION\t%s' % (reservation_string)
#    instances = []
#    for instance in reservation.instances:
#      if instance.id in instance_ids:
#        instances.append(instance)
#      else:
#        instances = reservation.instances
#    for instance in instances:
#      instance_num = instance_num + 1
#      try :
#        instance_name = Instances.objects.get(instance_id = instance.id).instance_name
#      except :
#        instance_name = ""
#      try :
#        instance_description = Instances.objects.get(instance_id = instance.id).instance_description
#      except :
#        instance_description = ""
#      try :
#        instance_tags = Instances.objects.get(instance_id = instance.id).instance_tags
#      except :
#        instance_tags = ""
#      if instance:
#        instance_image_name = ""
#        try :
#          instance_image_name = Machine_images.objects.get(image_id = instance.image_id).image_name
#        except :
#          instasnce_image_name = ""
#        instance_json_string = instance_json_string + """
#        {
#              "instance_num" : "%s" ,
#              "instance_name" : "%s" ,
#              "instance_description" : "%s",
#              "instance_tags" : "%s",
#              "reservation_id" : "%s" ,
#              "reservation_owner_id" : "%s" ,
#              "group_id" : "%s" ,
#              "instance_id" : "%s" ,
#              "instance_image_id": "%s" ,
#              "instance_image_name" : "%s" , 
#              "instance_public_dns_name" : "%s" ,
#              "instance_private_dns_name" : "%s" ,
#              "instance_state" : "%s" ,
#              "instance_key_name" : "%s" ,
#              "instance_ami_launch_index" : "%s" ,
#              "instance_product_codes" : "%s" ,
#              "instance_instance_type" : "%s" ,
#              "instance_launch_time" : "%s" ,
#              "instance_placement" : "%s" ,
#              "instance_kernel" : "%s" ,
#              "instance_ramdisk" : "%s"
#         }, """ % (
#              instance_num ,
#              instance_name ,
#              instance_description.replace("\n", "<br>"),
#              instance_tags , 
#              reservation.id,
#              reservation.owner_id ,
#              group.id,
#              instance.id,
#              instance.image_id,
#              instance_image_name,
#              instance.public_dns_name,
#              instance.private_dns_name,
#              instance.state,
#              instance.key_name,
#              instance.ami_launch_index,
#              instance.product_codes ,
#              instance.instance_type,
#              instance.launch_time,
#              instance.placement,
#              instance.kernel,
#              instance.ramdisk
#            )
#      return_json_str = "[%s]" % instance_json_string[0:-2]
#  #Monitor_instance_list
#  tasks = Tasks(task_name=inspect.stack()[0][3],task_result=''.join(return_json_str.splitlines()).replace('  ',''))
#  tasks.save()