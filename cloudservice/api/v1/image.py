#!/usr/bin/env python

#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


import getopt, sys, os
from euca2ools import Euca2ool, InstanceValidationError, SizeValidationError, SnapshotValidationError, VolumeValidationError, Util
from django.utils import simplejson
import logging
from atmosphere.cloudservice.models import *
import datetime
import uuid

from django.utils import simplejson
import atmosphere.cloudservice.api.v1.util as atmo_util

class Image :

  def registerImage(self,request):
    manifest_json = simplejson.loads(request.POST['manifest'])
    request_user = request.META['HTTP_X_AUTH_USER']
    
    # check required field's existance
    emi_id = manifest_json['image_id']
    # self.ec2_access_key
    # self.ec2_sec`    

    #euca_local = Euca2ool('s:z:', ['zone=', 'snapshot=', 'size='], compat=True)
    #ec2_user_access_key = self.ec2_access_key
    #ec2_user_secret_key = self.ec2_secret_key
    #ec2_url = self.ec2_url
    #s3_url = self.s3_url
    #euca_conn = euca_local.make_connection()
 
    euca_conn = self.euca.make_connection()
    images = euca_conn.get_all_images()
    logging.debug(images)
    image_list = []
    for image in images:
      image_list.append(image.id)
      if image.id in emi_id:
        #image.id, image.location, image.ownerId, image.state
        if request_user != image.ownerId:
          return atmo_util.jsoner("\"failed\"","\"\"","\"You don't have access to image %s\"" % emi_id)
          
    if emi_id not in image_list:
      return atmo_util.jsoner("\"failed\"","\"\"","%s" % "Image '"+emi_id+"' does not exit. Please upload/register image first")
    
    # ok done. Let's update database
    
    logging.debug(manifest_json['image_name'])
    logging.debug(manifest_json['image_description'])
    logging.debug(manifest_json['image_tags'])
    logging.debug(manifest_json['image_id'])
    logging.debug(request_user)
    logging.debug(manifest_json['image_ramdisk_id'])
    logging.debug(manifest_json['image_kernel_id'])
    logging.debug(manifest_json['atmo_init_script_id'])
    
    machine_image = Machine_images(
      image_name = manifest_json['image_name'],
      image_description = manifest_json['image_description'],
      image_tags = manifest_json['image_tags'],
      image_id = manifest_json['image_id'],
      image_ownerid = request_user,
      image_ramdisk_id = manifest_json['image_ramdisk_id'],
      image_kernel_id = manifest_json['image_kernel_id'],
      machine_image_user_data_scripts_script_id = manifest_json['atmo_init_script_id'],
      registered_at = datetime.datetime.now()
    )
    machine_image.save()
    
        
    #image.id
    #image.location
    #image.ownerId
    #image.state
    
 
 
 
 
    # check emi-id is new
    
    # check emi is really owned by user
    
    
    
    
    
    
    #logging.debug(">>>" + self.ec2_access_key)
    
    for key in manifest_json:
      #logging.debug(key + " > " + manifest_json[key])
      pass
    
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % "Success")
