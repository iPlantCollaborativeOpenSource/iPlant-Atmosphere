#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
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
from atmosphere.cloudservice.api.v1.cloudadmin import CloudAdmin
from atmosphere.cloudservice.api.v1.image import Image as atmo_image
import atmosphere.cloudservice.api.v1.util as atmo_util
from django.utils.encoding import smart_str
from django.utils.datastructures import MultiValueDictKeyError
import json


from datetime import datetime
from atmosphere.cloudservice.resources import create_resource_id


# I like to change this class better when I get time :-)
# it works now.. but not really code I like to show others


class Ec2_cloud(object, atmo_image):
  
  # this kind of class variable definition is not for python
  # need to fix this thing
  # but it works now so will fix later
  # seung-jin
  
  # this class is quite java-style
  # will fix more like python style later
  
  #euca = None
  #ec2_access_key = None
  #ec2_secret_key = None
  #ec2_url = None
  #s3_url = None

  def __init__(self,ec2_access_key, ec2_secret_key, ec2_url, s3_url):
   
    self.euca = Euca2ool()
    self.euca.ec2_user_access_key = str(ec2_access_key)
    self.euca.ec2_user_secret_key = str(ec2_secret_key)
    self.euca.ec2_url = ec2_url
    self.euca.s3_url = s3_url

    self.ec2_access_key = ec2_access_key
    self.ec2_secret_key = ec2_secret_key 
    self.ec2_url = ec2_url
    self.s3_url = s3_url
    
    self.userid = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key).username
  
  # this getters does not need in python
  # will fix later
  def getEc2AccessKey(self,req):
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % self.ec2_access_key)
  
  def getEc2SecretKey(self,req):
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % self.ec2_secret_key)
  
  def getEc2Url(self,req):
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % self.ec2_url)
  
  def getS3Url(self,req):
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % self.s3_url)
  
  def getUserId(self,req):
    # get userid based on ec2_access_key
    userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
    #return userinfo.username
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % userinfo.username)
  
  def getUserProfile(self,req):
    userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
    # TODO
    # quota info
    p = User_resource_quotas.objects.filter(userid=self.userid)
    if p.count() == 0 :
      cpu_limit = mem_limit = 'Unlimited'
    else :
      cpu_limit = p[0].cpu
      mem_limit = p[0].memory
    user_profile = '{"userid":"%s"},{"ec2_access_key":"%s"},{"ec2_secret_key":"%s"},{"ec2_url":"%s"},{"s3_url":"%s"},{"token":"%s"},{"api_server":"%s"},{"quota_cpu":"%s"},{"quota_mem":"%s"}' % (userinfo.username,self.ec2_access_key,self.ec2_secret_key,self.ec2_url,self.s3_url,req.META['HTTP_X_AUTH_TOKEN'],req.META['HTTP_X_API_SERVER'],cpu_limit,mem_limit)
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % user_profile)
    
  def getImageList(self, req):  
  # list image list
    image_ids = self.euca.process_args()
    image_json_string = ""
    euca_conn = self.euca.make_connection()
    images = euca_conn.get_all_images()
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
        image_json_string = image_json_string +"""{ "image_name" : "%s", "image_description" : "%s", "image_tags" : "%s", "image_id" : "%s" , "image_location" : "%s" , "image_ownerid" : "%s" , "image_state" : "%s" ,"image_is_public" : "%s" ,"image_product_codes" : "%s" ,"image_architecture" : "%s" ,"image_type" : "%s","image_ramdisk_id" : "%s","image_kernel_id" : "%s", "image_condition" : "%s", "image_type" : "%s" , "image_condition" : "%s" }, """ % (
          image_name,
          image_description,
          image_tags,
          image.id,
          image.location,
          image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id, image_condition, image_type, image_condition
        )
    
    # eucalyptus bug
    # users can see other user's private image. even they can launch it. so atmosphere hides private image of other users.
    my_available_image = filter(lambda e: e['image_is_public'] == 'public' or e['image_ownerid'] == self.userid, json.loads("["+image_json_string[0:-2]+"]"))
    return atmo_util.jsoner("\"success\"","\"\"","%s" % json.dumps(my_available_image))


  def getInstanceList(self, req) :
    return_json_str = "[]";
    euca_conn = self.euca.make_connection()
    try :
      reservations = euca_conn.get_all_instances()
    except Exception, ex:
      logging.error('cloud.py : ' + ex)
      #euca.disaply_error_and_exit('%s' % ex)
    
    instance_ids = ""
    instance_num = 0
    instance_json_string = ""
    # reservation
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
      #return_json_str = "[%s]" % instance_json_string[0:-2]
      return_json_str = instance_json_string[0:-2]
    queued_instances = Instances.objects.filter(owner_id="seungjin",current_state="queued")
    if len(queued_instances) > 0 :
      queued_instance_json_string = ""
      for queued_instance in queued_instances:
        instance_num = instance_num + 1
        queued_instance_json_string = queued_instance_json_string + """
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
            instance_num,
            queued_instance.instance_name ,
            queued_instance.instance_description.replace("\n", "<br>"),
            queued_instance.instance_tags , 
            queued_instance.reservation,
            queued_instance.owner_id ,
            queued_instance.group_id,
            queued_instance.instance_id,
            queued_instance.machine_image,
            None,
            queued_instance.public_dns_name,
            queued_instance.private_dns_name,
            queued_instance.current_state,
            queued_instance.key_name,
            queued_instance.ami_index,
            queued_instance.product_code ,
            queued_instance.machine_size,
            "",
            queued_instance.placement,
            queued_instance.kernel,
            queued_instance.ramdisk
          )
      b = "[" + return_json_str + ", " + queued_instance_json_string[0:-2] + "]"
    else :
      b = "[" + return_json_str +"]"
    a = simplejson.loads(b)
    #return simplejson.dumps(a)

    return atmo_util.jsoner("\"success\"","\"\"", simplejson.dumps(a))

  def getRunningInstancesTree(self, req):
    euca_conn = self.euca.make_connection()
    try :
      reservations = euca_conn.get_all_instances()
    except Exception, ex:
      euca.disaply_error_and_exit('%s' % ex)
    
    instance_ids = ""
    instance_num = 0
    instance_json_string = ""
    
    # reservation
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
        if instance.state == "running":
          try :
            instance_name = Instances.objects.get(instance_id = instance.id).instance_name
          except :
            instance_name = ""
          instance_json_string = instance_json_string + """
            {
              "id" : "%s" ,
              "text" : "%s (%s)" ,
              "leaf" : "false"
            }, """ % (
              instance_num ,
              instance_name , 
              instance.id
            )
    return_json_str = "[%s]" % instance_json_string[0:-2]
    #return return_json_str
    return atmo_util.jsoner("\"success\"","\"\"",return_json_str)
    
  def launchInstance(self, req) :
    this_function_name = "launchInstance"
    if req.method == "POST":
      req_item_list = [];
      for i in req.POST.iteritems(): req_item_list.append(i[0])

      #should be nicely done by dynamically. ugly hugh
        
      if u'instance_size' in req_item_list : instance_type = req.POST['instance_size']
      else : return atmo_util.jsoner("\"fail\"","\"\"","\"%s\"" % "required parameter 'instance_size' missing")

      #if u'num_of_instances' in req_item_list : min_count = str(req.POST['num_of_instances'])
      #else : min_count = u'1'
      #min_count = req.POST['num_of_instances'] if req.POST['num_of_instances'] else 1
      
      #if u'num_of_instances' in req_item_list : max_count = str(req.POST['num_of_instances'])
      #else : max_count = u'1'
      #max_count = req.POST['num_of_instances'] if req.POST['num_of_instances'] else 1
      max_count = 1
      min_count = 1
      
      if u'num_of_instances' in req_item_list :
       if (req.POST['num_of_instances'] == None) or (req.POST['num_of_instances'].strip() == "")  :
        max_count = min_count = 1
       else :
        max_count = req.POST['num_of_instances'] 
        min_count = req.POST['num_of_instances']   
        
      if u'callback_resource_url' in req_item_list : callback_resource_url = req.POST['callback_resource_url']
      else : callback_reousrce_url = None
 
      requested_cpu = int(self.convertMachineTypeStringToNum(instance_type)['cpu']) * int(max_count)
      requested_mem = int(self.convertMachineTypeStringToNum(instance_type)['mem']) * int(max_count)
      quota_check = self.checkEc2ResourceQuota(newly_requested_cpu=requested_cpu,newly_requested_mem=requested_mem)
      if quota_check['result'] == "unavailable" :
        quota_check_json = '{"limit_cpu":%s, "limit_mem":%s, "current_cpu":%s, "current_mem":%s }' % (quota_check['limit_cpu'], quota_check['limit_mem'], quota_check['current_cpu'], quota_check['current_mem'])
        return atmo_util.jsoner("\"fail\"","\"quota over\"",quota_check_json)

      #logging.debug(self.convertMachineTypeStringToNum(instance_type)['cpu'])
      # quota check ends
      
      if u'image_id' in req_item_list : image_id = req.POST['image_id']
      else : return atmo_util.jsoner("\"fail\"","\"\"","\"%s\"" % "required parameter 'image_id' missing")
      #image_id = req.POST['image_id'] if req.POST['image_id'] else None
      
      if u'auth_key' in req_item_list : keyname = req.POST['auth_key']
      else : return atmo_util.jsoner("\"fail\"","\"\"","\"%s\"" % "required parameter 'auth_key' missing")
      #keyname = req.POST['auth_key']

      if u'instance_lifetime' in req_item_list : lifetime = req.POST['instance_lifetime']
      else : lifetime = -1
      
      kernel_id = None
      ramdisk_id = None
      group_names = [ ]
      user_data = None
      user_data_file = None
      addressing_type = None
      zone = None
 
      #user_data_file = open(os.path.abspath(os.path.dirname(__file__))+'/../../api/v1/atmo-init.rb', 'r')
      #user_data = user_data_file.read()
      #user_data_file.close()

      # default user_data?
      # what if user_data is null??
      
      if len(Machine_images.objects.filter(image_id = image_id)) > 0 :
        #user_data = Machine_image_userdata_scripts.objects.get(script_id=(Machine_images.objects.get(image_id = image_id).machine_image_user_data_scripts_script_id)).script
        user_data = Machine_image_userdata_scripts.objects.get(script_id=(Machine_images.objects.filter(image_id = image_id).order_by('-id')[0].machine_image_user_data_scripts_script_id)).script
      else:
        user_data = None
      
      num_req_inst = int(max_count)
      for a in range(0,num_req_inst):
        instance_token = str(uuid.uuid4())
        instance_service_url = Configs.objects.get(key="instance_service_url").value
        userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
        instance_config = """{
        "atmosphere":{  "servicename":"instance service",
                    "instance_service_url":"%s",
                    "token":"%s",
                    "userid":"%s",
                    "instance_name":"%s", 
                    "image_id":"%s",
                    "instance_tags":"%s", 
                    "lifetime":"%s",
                    "launched_by":"%s"
                  }
        }""" % (
          instance_service_url,
          instance_token,
          userinfo.username,
          req.POST['instance_name'],
          image_id,
          req.POST['instance_tags'],
          req.POST['instance_lifetime'],
          this_function_name
        )

        user_data = user_data + "\narg = '" + instance_config + "'\nmain(arg)\n\n"
        atmosphere_resource_id = create_resource_id('instance')

        inst = Instances(
          atmosphere_resource_id = atmosphere_resource_id,
          instance_name = req.POST['instance_name'],
          instance_description = req.POST['instance_description'],
          instance_tags = req.POST['instance_tags'],
          owner_id = self.userid,
          machine_image = image_id,
          current_state = "queued",
          machine_size = instance_type,
          launch_request_time = datetime.now(),
          launched_by = this_function_name,
          lifetime = lifetime,
          instance_token = instance_token,
          user_data = user_data
        )
        inst.save()

        instance_lifecycles = Instance_lifecycles(
          atmosphere_resource_id = atmosphere_resource_id,
          #instance_id = instance.id,
          #previous_instance_lifecycles_id = 
          #instance_launched_at = 
          instance_lifetime = lifetime
          #instance_terminated_at = 
          #instance_terminated_by =  
        )
        instance_lifecycles.save()
        if u'callback_resource_url' in req_item_list :
          ilh = Instance_launch_hooks(
              instance_id = instance.id,
              owner_id = reservation.owner_id,
              webhook_url = req.POST['callback_resource_url'], 
              webhook_header_params = None,
              requested_time = datetime.now()
          )
          ilh.save()
      return atmo_util.jsoner("\"success\"","\"\"","\"%s\""  % atmosphere_resource_id)
    else:
      return atmo_util.jsoner("\"fail\"","\"expecting post method but not received it\"","\"\"")


#      instance_token = str(uuid.uuid4())
#      instance_service_url = Configs.objects.get(key="instance_service_url").value
#      userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
#      instance_config = """{
#      "atmosphere":{  "servicename":"instance service",
#                      "instance_service_url":"%s",
#                      "token":"%s",
#                      "userid":"%s",
#                      "instance_name":"%s",
#                      "image_id":"%s",
#                      "instance_tags":"%s", 
#                      "lifetime":"%s",
#                      "launched_by":"%s"
#                    }
#      }""" % ( instance_service_url, instance_token, userinfo.username, req.POST['instance_name'], image_id, req.POST['instance_tags'],req.POST['instance_lifetime'],this_function_name)
#      
#      if user_data != None :
#        user_data = user_data + "\narg = '" + instance_config + "'\nmain(arg)\n\n"
#      else :
#        user_data = ""
#        
#      euca_conn = self.euca.make_connection()
#      try :
#        reservation = euca_conn.run_instances (
#          image_id = image_id,
#          min_count = min_count,
#          max_count = max_count,
#          key_name = keyname,
#          security_groups = group_names,
#          user_data = user_data,
#          addressing_type = addressing_type,
#          instance_type = instance_type,
#          placement = zone,
#          kernel_id = kernel_id,
#          ramdisk_id = ramdisk_id
#        )
#      except Exception, e:
#        return atmo_util.jsoner("\"fail\"","\"\"","\"%s\"" % e)
#
#      instance_id = None
#      for group in reservation.groups:
#        for instance in reservation.instances:
#          inst = Instances(
#            instance_name = req.POST['instance_name'],
#            instance_description = req.POST['instance_description'],
#            instance_tags = req.POST['instance_tags'],
#            reservation = reservation.id ,
#            owner_id = reservation.owner_id,
#            group_id = group.id,
#            instance_id = instance.id ,
#            machine_image = instance.image_id,
#            public_dns_name = instance.public_dns_name,
#            private_dns_name = instance.private_dns_name,
#            current_state = instance.state,
#            ami_index = instance.ami_launch_index,
#            product_code = instance.product_codes,
#            machine_size = instance.instance_type,
#            placement = instance.placement,
#            key_name = instance.key_name,
#            launch_time = instance.launch_time,
#            kernel = instance.kernel,
#            ramdisk = instance.ramdisk,
#            launched_by = this_function_name,
#            launch_request_time = datetime.now(),
#            lifetime = req.POST['instance_lifetime'],
#            instance_token = instance_token,
#            launch_response_time = None
#          )
#          instance_id = instance.id
#          inst.save()
#
#          instance_lifecycles = Instance_lifecycles(
#            instance_id = instance.id,
#            #previous_instance_lifecycles_id = 
#            #instance_launched_at = 
#            instance_lifetime = req.POST['instance_lifetime']
#            #instance_terminated_at = 
#            #instance_terminated_by =  
#          )
#          instance_lifecycles.save()
#
#          if u'callback_resource_url' in req_item_list :
#            ilh = Instance_launch_hooks(
#              instance_id = instance.id,
#              owner_id = reservation.owner_id,
#              webhook_url = req.POST['callback_resource_url'], 
#              webhook_header_params = None,
#              requested_time = datetime.now()
#            )
#            ilh.save()
#      return atmo_util.jsoner("\"success\"","\"\"","\"%s\""  % str(instance_id ))
#    else:
#      return atmo_util.jsoner("\"fail\"","\"expecting post method but not received it\"","\"\"")
    
    
  def terminateInstance(self, req) :
    if req.method == "POST" :
      euca_conn = self.euca.make_connection()
      instance_ids = []
      instance_ids.append(req.POST['instance_id'])
      print instance_ids
      try :
        euca_conn.terminate_instances(instance_ids)
      except Exception, ex:
        print ex
      
      # update status in my db
      try:
        current_time = datetime.now()
        e = Instances.objects.get(instance_id = req.POST['instance_id'])
        e.current_state = 'terminated'
        e.termination_request_time = current_time 
        e.save()
        terminated_instance = Instance_lifecycles.objects.get(instance_id = req.POST['instance_id'])
        terminated_instance.instance_terminated_at = current_time
        terminated_instance.instance_terminated_by = "terminateInstance"
        terminated_instance.save()
      except : 
        pass
    return atmo_util.jsoner("\"success\"","\"\"","\"\"")
  
  def getKeyPairsList(self, req) :
    
    euca_conn = self.euca.make_connection()
    keypairs = euca_conn.get_all_key_pairs()
    keypairs_list = ''
    for keypair in keypairs :
      keypair_string = """{"keypair_name" : "%s", "keypair_fingerprint" : "%s"},\n""" % (keypair.name, keypair.fingerprint)
      keypairs_list = keypairs_list + keypair_string
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % keypairs_list[0:-2])
  
  def getKeyPairsListTree(self, req) :
    euca_conn = self.euca.make_connection()
    keypairs = euca_conn.get_all_key_pairs()
    keypairs_list = ''
    keypair_id = 0
    for keypair in keypairs :
      keypair_id = keypair_id + 1
      keypair_string = """{"id" : "%s", "text" : "%s", "leaf" : "false"},""" % (keypair_id,keypair.name)
      keypairs_list = keypairs_list + keypair_string
    #print atmo_util.jsoner(keypairs_list[0:-1])
    #return "[%s]" % keypairs_list[0:-1]
    logging.debug(keypairs_list)
    return atmo_util.jsoner("\"success\"","null","[%s]" % keypairs_list[0:-1])
  
  def createKeyPair(self, req) :
    logging.debug(req)
    euca_conn = self.euca.make_connection()
    keypair = None
    logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
    keypair_name = userinfo.username + "_" +req.POST['keypair_name']
    #logging.debug(">>>>>>")
    #logging.debug(keypair_name)
    keypair = euca_conn.create_key_pair(keypair_name)
    #logging.debug(keypair.material.replace('\n','\\n'))
    key_string = keypair.material.replace('\n','\\n');
    keypair_string = '%s\\t%s\\t%s' % (keypair.name, keypair.fingerprint, key_string)
    return atmo_util.jsoner("\"success\"","null","\"%s\"" % keypair_string)

  def removeKeyPair(self, req) :
    euca_conn = self.euca.make_connection()
    keypair = euca_conn.delete_key_pair(req.POST['keypair_name'])
    if keypair == True:
      return atmo_util.jsoner("\"success\"","\"\"","\"\"")
    else :
      return "2"
    
  def getVolumeListTree(self, reg) :
    logging.debug("_seungjin_ getVolumeListTree called")
    euca_conn = self.euca.make_connection()
    volumes = euca_conn.get_all_volumes()
    
    volume_json_string = u''
    volume_no = 0
    for volume in volumes:
      volume_no = volume_no + 1
      try :
        volume_name = Machine_volumes.objects.get(volume_id = volume.id).volume_name
      except :
        volume_name = ""
      volume_json_string = volume_json_string + """
        {
          "id" : "%s",
          "text" : "%s (%s)",
          "leaf" : "false"
        }, """ % (
          volume_no ,
          volume_name ,
          volume.id ,
        )
    #return "["+volume_json_string[0:-2]+"]"
    return atmo_util.jsoner("\"success\"","\"\"","%s" % "["+volume_json_string[0:-2]+"]")  
 
  def getMachineImageTree(self,req):
    image_ids = self.euca.process_args()
    image_json_string = ""
    euca_conn = self.euca.make_connection()
    images = euca_conn.get_all_images()
    image_no = 0
    for image in images :
      if ( (image.type == "machine") and image.is_public ) or ( (image.type == "machine") and (image.ownerId == self.userid) ) :
        # atmosphere info
        try :
          machine_image_name = Machine_images.objects.get(image_id = image.id).image_name
        except :
          machine_image_name = ""
        # end of atmos info
        image_no = image_no + 1
        #image.id, image.location, image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id
        if image.is_public:
          image.is_public = "public"
        else :
          image.is_puiblic = "private"
        image_json_string = image_json_string +"""
        {
          "id" : "%s",
          "text" : "%s (%s)",
          "leaf" : "false"
        }, """ % (
          image_no, machine_image_name, image.id
        )
    r = "[%s]" % image_json_string[0:-2]
    #return r
    return atmo_util.jsoner("\"success\"","\"\"","%s" % r)

  def getVolumeList(self,req) :
    logging.debug("_seungjin_ method call : getVolumeList")
    euca_conn = self.euca.make_connection()
    volumes = euca_conn.get_all_volumes()
    volume_json_string = u''
    volume_no = 0
    for volume in volumes:
      volume_no = volume_no + 1
      try :
        volume_name = Machine_volumes.objects.get(volume_id = volume.id).volume_name
      except :
        volume_name = ""
      try :
        volume_description = Machine_volumes.objects.get(volume_id = volume.id).volume_description
      except :
        volume_description = ""
      try :
        volume_tags = Machine_volumes.objects.get(volume_id = volume.id).volume_tags
      except :
        volume_tags = ""
      
      volume_descriptoin_html = volume_description.replace("\n", "<br>") if volume_description is not None else ""
      volume_json_string = volume_json_string + """
        {
          "no" : "%s",
          "name" : "%s",
          "description" : "%s",
          "tags" : "%s" ,
          "id" : "%s",
          "size" : "%s",
          "snapshot_id" : "%s",
          "status" : "%s",
          "create_time" : "%s" ,
          "attach_data_instance_id" : "%s" ,
          "attach_data_device" : "%s" , 
          "attach_data_attach_time" : "%s"
        }, """ % (
          volume_no ,
          volume_name ,
          volume_descriptoin_html ,
          volume_tags,
          volume.id ,
          volume.size ,
          volume.snapshot_id,
          volume.status,
          volume.create_time, 
          volume.attach_data.instance_id,
          volume.attach_data.device, 
          volume.attach_data.attach_time
        )
    logging.debug("_seungjin_ 2" + "["+volume_json_string[0:-2]+"]")
    #return "["+volume_json_string[0:-2]+"]"
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % volume_json_string[0:-2])
  def attachVolume(self,req) :
    if req.method == "POST":
      instance_id = req.POST['instance_id']
      device = req.POST['device']
      volume_id = req.POST['volume_id']
      try:
        euca = Euca2ool('i:d:', ['instance=', 'device='])
      except Exception, e:
        logging.error(e)
      #euca_conn = euca.make_connection()
      euca_conn = self.euca.make_connection()
      try:
        return_code = euca_conn.attach_volume(volume_id = volume_id, instance_id = instance_id, device = device)
      except Exception, ex:
        logging.error(ex)
      return atmo_util.jsoner("\"success\"","\"\"", simplejson.dumps(return_code))
    else :
      return atmo_util.jsoner("\"failed\"","\"\"", simplejson.dumps("invalid method"))
  
  def detachVolume(self,req) :
    if req.method == "POST":
      instance_id = req.POST['instance_id']
      volume_id = req.POST['volume_id']
      try:
        euca = Euca2ool('i:d:', ['instance=', 'device=']) 
      except Exception, e:
        logging.error(e)
      #euca_conn = euca.make_connection()
      euca_conn = self.euca.make_connection()
      try:
        return_code = euca_conn.detach_volume(volume_id = volume_id)
      except Exception, ex:
        logging.error(ex)
      return atmo_util.jsoner("\"success\"","\"\"", simplejson.dumps(return_code))

  def getVmTypes(self,req) :
    ca = CloudAdmin()
    r = ""
    for type in ca.getInstanceTypeSize() : r += """{"name" : "%s" , "cpus" : "%s" , "memory" : "%s" , "disc" : "%s"},""" % (type[1],type[2],type[3],type[4])
    return atmo_util.jsoner("\"success\"","\"\"", "["+r[:-1]+"]")
  
  def getInstanceInfo(self, req) :
    
    euca_conn = self.euca.make_connection()
    logging.error(req);
    instance_id_list = []
    instance_id_list.append(req.POST['instance_id'])
    try :
      reservations = euca_conn.get_all_instances(instance_id_list)
    except Exception, ex:
      euca.disaply_error_and_exit('%s' % ex)
    
    instance_ids = ""
    instance_num = 0
    instance_json_string = ""
    # reservation
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
    a = simplejson.loads(return_json_str)
    #return simplejson.dumps(a)
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % simplejson.dumps(a))

  def getAttachedVolumeList(self,req) :
    #euca = Euca2ool()
    euca_conn = self.euca.make_connection()
    volumes = euca_conn.get_all_volumes()
    volume_json_string = u''
    volume_no = 0
    for volume in volumes:
      volume_no = volume_no + 1
      try :
        volume_name = Machine_volumes.objects.get(volume_id = volume.id).volume_name
      except :
        volume_name = ""
      try :
        volume_description = Machine_volumes.objects.get(volume_id = volume.id).volume_description
      except :
        volume_description = ""
      try :
        volume_tags = Machine_volumes.objects.get(volume_id = volume.id).volume_tags
      except :
        volume_tags = ""
      volume_json_string = volume_json_string + """
        {
          "no" : "%s",
          "name" : "%s",
          "description" : "%s",
          "tags" : "%s" ,
          "id" : "%s",
          "size" : "%s",
          "snapshot_id" : "%s",
          "status" : "%s",
          "create_time" : "%s" ,
          "attach_data_instance_id" : "%s" ,
          "attach_data_device" : "%s" , 
          "attach_data_attach_time" : "%s"
        }, """ % (
          volume_no ,
          volume_name ,
          volume_description.replace("\n", "<br>"),
          volume_tags,
          volume.id ,
          volume.size ,
          volume.snapshot_id,
          volume.status,
          volume.create_time, 
          volume.attach_data.instance_id,
          volume.attach_data.device, 
          volume.attach_data.attach_time
        )
    #return "["+volume_json_string[0:-2]+"]"
    return atmo_util.jsoner("\"success\"","\"\"","[%s]" % volume_json_string[0:-2])

  def createVolume(self,req):
    #euca-create-volume -S, --size size | --snapshot snapshot_id -z zone
    # for current system. zone is fixed. zone=iplant
    size = None
    zone = "bespin"
    snaphost_id = None
    name = None
    description = None
    tags = None
    volume_id = None
    
    if req.method == "POST" :
      size = req.POST['size']
      name = req.POST['name']
      description = req.POST['description']
      tags = req.POST['tags']
    else:
      return "method not valid"
    
    euca_local = Euca2ool('s:z:', ['zone=', 'snapshot=', 'size='], compat=True)
    euca_local.ec2_user_access_key = self.ec2_access_key
    euca_local.ec2_user_secret_key = self.ec2_secret_key
    euca_local.ec2_url = self.ec2_url
    euca_local.s3_url = self.s3_url
    euca_conn = euca_local.make_connection()
    
    try:
      euca_local.validate_volume_size(int(size))
    except SizeValidationError:
      print 'Invalid volume size'
    
    try:
      volume = euca_conn.create_volume(size,zone,snaphost_id)
      if volume:
        volume_id = str(volume).split(":")[1]
    except Exception, ex:
      print ex
    
    machine_volume = Machine_volumes(
      volume_name = name,
      volume_description = description,
      volume_tags = tags,
      volume_id = volume_id,
      volume_size = size,
      volume_snapshot_id = snaphost_id,
      volume_status = None,
      volume_create_time = datetime.now()
    )
    machine_volume.save()
      
    return atmo_util.jsoner("\"success\"","null","[\"%s\"]" % volume_id)
    
  def deleteVolume(self, req):
    volume_id = None
    volume_id = req.POST['volume_id']
    
    if volume_id :
      try:
        self.euca.validate_volume_id(volume_id)
      except VolumeValidationError:
        print "invalid volume id"
          
      euca_conn = self.euca.make_connection()
    try:
      return_code = euca_conn.delete_volume(volume_id)
    except Exception, ex:
      print ex
    return atmo_util.jsoner("\"success\"","\"\"","\"\"")
    
  def getAppList(self, req):
    logging.debug("getAppList called")
    #application_stacks = Applications.objects.all()
    application_stacks = Applications.objects.order_by('application_name')
    applications_json = ""
    for o in application_stacks:
      logging.debug(o.application_name)
      applications_json = applications_json+ """{
          "application_name":"%s",
          "application_icon_path":"%s",
          "application_id":"%s",
          "application_creator":"%s",
          "application_created":"%s",
          "application_version":"%s",
          "application_category":"%s",
          "application_type":"%s",
          "platform":"%s",
          "machine_image_id":"%s",
          "kernel_id":"%s",
          "ramdisk_id":"%s",
          "system_minimum_requirements":"%s",
          "application_tags":"%s",
          "application_description":"%s",
          "application_lifetime":"%s",
          "is_sys_app":true
        }, """ % (
        o.application_name,
        o.application_icon_path,
        o.application_id,
        o.application_creator,
        o.application_created,
        o.application_version,
        o.application_category,
        o.application_type,
        o.platform,
        o.machine_image_id,
        o.kernel_id,
        o.ramdisk_id,
        o.system_minimum_requirements,
        o.application_tags,
        o.application_description.replace('\n', ''),
        o.application_lifetime
      )
    
    #user application stacks
    user_application_stacks = User_applications.objects.filter(user_id=self.userid).order_by('application_order')
    for p in user_application_stacks:
      applications_json = applications_json+ """{
          "application_name":"%s",
          "application_icon_path":"%s",
          "application_id":"u_%s",
          "application_creator":"%s",
          "application_created":"%s",
          "application_version":"%s",
          "application_category":"%s",
          "application_type":"%s",
          "platform":"%s",
          "machine_image_id":"%s",
          "kernel_id":"%s",
          "ramdisk_id":"%s",
          "system_minimum_requirements":"%s",
          "application_tags":"%s",
          "application_description":"%s",
          "application_lifetime":"%s",
          "application_order":"%s",
          "is_sys_app":false
        }, """ % (
        p.application_name,
        p.application_icon_path,
        p.application_id,
        p.user_id,
        p.application_created,
        p.application_version,
        p.application_category,
        p.application_type,
        p.platform,
        p.machine_image_id,
        p.kernel_id,
        p.ramdisk_id,
        p.system_minimum_requirements,
        p.application_tags,
        p.application_description,
        p.application_lifetime,
        p.application_order
      )
      
    return atmo_util.jsoner("\"success\"","null","["+applications_json[0:-2]+"]")

  def launchApp(self, req):
    # euca-run-instance -t m1.small -z iplanto1 -f atmo-init.rb emi-123
    this_function_name = "launchApp"
    if req.method == "POST":
      # quota check starts
      instance_type = req.POST['instance_size']
      min_count = 1
      max_count = 1
      requested_cpu = int(self.convertMachineTypeStringToNum(instance_type)['cpu']) * int(max_count)
      requested_mem = int(self.convertMachineTypeStringToNum(instance_type)['mem']) * int(max_count)
      quota_check = self.checkEc2ResourceQuota(newly_requested_cpu=requested_cpu,newly_requested_mem=requested_mem)
      if quota_check['result'] == "unavailable" :
        quota_check_json = '{"limit_cpu":%s, "limit_mem":%s, "current_cpu":%s, "current_mem":%s }' % (quota_check['limit_cpu'], quota_check['limit_mem'], quota_check['current_cpu'], quota_check['current_mem'])
        return atmo_util.jsoner("\"fail\"","\"quota over\"",quota_check_json)
      instance_name = req.POST['instance_name']
      image_id = req.POST['image_id'] if req.POST['image_id'] else None
      keyname = None
      kernel_id = None
      ramdisk_id = None
      instance_type = req.POST['instance_size']
      group_names = [ ]
      user_data = None
      user_data_file = None
      addressing_type = None
      zone = None
      
      
      #user_data_file = open(os.path.abspath(os.path.dirname(__file__))+'/../../api/v1/atmo-init.rb', 'r')
      #user_data = user_data_file.read()
      #user_data_file.close()

      if req.POST['application_id'][:2] == "u_" :
        user_app_id = req.POST['application_id'][2:]
        user_data = Machine_image_userdata_scripts.objects.get(script_id=(User_applications.objects.get(application_id = user_app_id)).machine_image_user_data_scripts_script_id).script
        lifetime = User_applications.objects.get(application_id = user_app_id).application_lifetime
      else :
        user_data = Machine_image_userdata_scripts.objects.get(script_id=(Applications.objects.get(application_id = req.POST['application_id']).machine_image_user_data_scripts_script_id)).script
        try: 
          lifetime = req.POST['instance_lifetime']
        except MultiValueDictKeyError, e:
          lifetime = Applications.objects.get(application_id = req.POST['application_id']).application_lifetime
      
      #logging.debug(user_data)
      
      instance_token = str(uuid.uuid4())
      instance_service_url = Configs.objects.get(key="instance_service_url").value
      userinfo = Ec2_keys.objects.get(ec2_access_key = self.euca.ec2_user_access_key)
      instance_config = """{
      "atmosphere":{  "servicename":"instance service",
                      "instance_service_url":"%s",
                      "token":"%s",
                      "userid":"%s",
                      "instance_name":"%s", 
                      "image_id":"%s",
                      "instance_tags":"%s", 
                      "lifetime":"%s",
                      "launched_by":"%s"
                    }
      }""" % (
        instance_service_url,
        instance_token,
        userinfo.username,
        req.POST['instance_name'],
        image_id,
        Applications.objects.get(application_id = req.POST['application_id']).application_tags,
        Applications.objects.get(application_id = req.POST['application_id']).application_lifetime,
        this_function_name
      )

      user_data = user_data + "\narg = '" + instance_config + "'\nmain(arg)\n\n"

      atmosphere_resource_id = create_resource_id('instance')

      inst = Instances(
        atmosphere_resource_id = atmosphere_resource_id,
        instance_name = req.POST['instance_name'],
        instance_description = "Atmosphere application\nLaunched by Atmosphere APP launcher",
        instance_tags = Applications.objects.get(application_id = req.POST['application_id']).application_tags,
        owner_id = self.userid,
        machine_image = image_id,
        current_state = "queued",
        machine_size = instance_type,
        launch_request_time = datetime.now(),
        launched_by = this_function_name,
        lifetime = lifetime,
        instance_token = instance_token,
        user_data = user_data
      )
      inst.save()

      instance_lifecycles = Instance_lifecycles(
        atmosphere_resource_id = atmosphere_resource_id,
        #instance_id = instance.id,
        #previous_instance_lifecycles_id = 
        #instance_launched_at = 
        instance_lifetime = lifetime
        #instance_terminated_at = 
        #instance_terminated_by =  
      )
      instance_lifecycles.save()

      return atmo_util.jsoner("\"success\"","\"\"","\"%s\""  % atmosphere_resource_id)
    else:
      return atmo_util.jsoner("\"fail\"","\"expecting post method but not received it\"","\"\"")

  def checkEc2ResourceQuota(self,newly_requested_cpu=0,newly_requested_mem=0): # return true / false
    # get user quota / no quota info means no quota (unlimited use)
    p = User_resource_quotas.objects.filter(userid=self.userid)
    if p.count() == 0 :
      cpu_limit = mem_limit = -1
    else :
      cpu_limit = p[0].cpu
      mem_limit = p[0].memory
    # get current instances and total resource uses / sum all cpus and all mem
    if (cpu_limit != -1) and (mem_limit != -1) :
      ca = CloudAdmin()
      machine_types = ca.getInstanceTypeSize()
      euca_conn = self.euca.make_connection()
      try :
        reservations = euca_conn.get_all_instances() # <- not from euca_conn but from db table. db table includes queued resources as well
      except Exception, ex:
        euca.disaply_error_and_exit('%s' % ex)
      # reservation
      current_cpu_use = current_mem_use = 0
      for reservation in reservations:
        for instance in reservation.instances:
          for mt in machine_types :
            if instance.instance_type == mt[1] :
              current_cpu_use += int(mt[2])
              current_mem_use += int(mt[3])
      if (cpu_limit >= current_cpu_use+newly_requested_cpu) and (mem_limit >= current_mem_use+newly_requested_mem):
        quotaAvailability = { "result" : "available" }
      else :
        quotaAvailability = { "result" : "unavailable", "current_cpu": current_cpu_use, "current_mem": current_mem_use, "limit_cpu" : cpu_limit, "limit_mem": mem_limit }
    elif (cpu_limit == -1) and (mem_limit == -1) :
      # unlimited resource
      quotaAvailability = { "result" : "available" }
    return quotaAvailability
  
  def convertMachineTypeStringToNum(self,machine_type):
    ca = CloudAdmin()
    machine_types = ca.getInstanceTypeSize()
    return_value = None;
    for mt in machine_types:
      if machine_type == mt[1] :
          return_value = {"cpu":mt[2],"mem":mt[3]}
    return return_value

  def getMethodsList(self):
    return atmo_util.jsoner("\"fail\"","\"not yet implemented\"","\"\"")

  def createInstanceAsImage(self):
    import sys
    #from euca2ools import Euca2ool, Util, InstanceValidationError ConnectionFailed
    import base64
    from datetime import datetime, timedelta
    
    #key:
    """
    try:
      bundle_task = euca_conn.bundle_instance(instance_id = instance_id, s3_bucket=bucket, s3_prefix=prefix, s3_upload_policy=policy)
    except Exception, ex:
      euca.display_error_and_exit('%s' % ex)

    """
    pass

  def extendInstanceLifetime(self, req) :
    # check request owner is actual user of the instance!
    #if ( == self.userid) : 
    
    # get instance_id
    instance_id = req.POST['instance_id']
    # get lifetime
    instance_lifetime = req.POST['instance_lifetime']
    # update instances table
    instance = Instances.objects.get(instance_id = instance_id)
    instance.lifetime = instance.lifetime +","+lifetime
    instance.lifetime.save()
    # update instance_lifecycles table
    instance_lifecycle = Instance_lifecycles.objects.get(instance_id = instance_id)
    instance_lifecycle.instance_id
    instance_lifecycle.instance_lifetime = instance_lifetime
    instance_lifecycle.save()