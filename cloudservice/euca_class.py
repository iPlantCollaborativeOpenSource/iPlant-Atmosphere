#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

import getopt, sys, os
from euca2ools import Euca2ool, InstanceValidationError, Util
from django.utils import simplejson
import logging
from atmosphere.cloudservice.models import *

class Cloud(object):
  
  ec2_url = 'http://150.135.78.126:8773/services/Eucalyptus'
  s3_url = 'http://150.135.78.127:8773/services/Walrus'
  
  def __init__(self,ec2_access_key, ec2_secret_key):
    os.environ['EC2_ACCESS_KEY'] = ec2_access_key
    os.environ['EC2_SECRET_KEY'] = ec2_secret_key
    os.environ['EC2_URL'] = self.ec2_url
    os.environ['S3_URL'] = self.s3_url
  
  def getImages(self, req):
  # list image list
    euca = Euca2ool()
    image_ids = euca.process_args()
    image_json_string = ""
    euca_conn = euca.make_connection()
    images = euca_conn.get_all_images()
    for image in images :
      if image.type == "machine" :
        # get atmosphere info
        try :
          image_name = Machine_images.objects.get(image_id = image.id).image_name
        except :
          image_name = ""
        try :
          image_description = Machine_images.objects.get(image_id = image.id).image_description
          if image_description == None :
            image_descriontino = ""
        except:
          image_description = ""
        try :
          image_tags = Machine_images.objects.get(image_id = image.id).image_tags
          if image_tags == None :
            image_tags = ""
        except :
          image_tags = "no tags"
        #image.id, image.location, image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id
        if image.is_public:
          image.is_public = "public"
        else :
          image.is_puiblic = "private"
        image_json_string = image_json_string +"""
        {
          "image_name" : "%s",
          "image_description" : "%s",
          "image_tags" : "%s",
          "image_id" : "%s" ,
          "image_location" : "%s" ,
          "image_ownerid" : "%s" ,
          "image_state" : "%s" ,
          "image_is_public" : "%s" ,
          "image_product_codes" : "%s" ,
          "image_architecture" : "%s" ,
          "image_type" : "%s" ,
          "image_ramdisk_id" : "%s" ,
          "image_kernel_id" : "%s"
        }, """ % (
          image_name,
          image_description.replace("\n", "<br>"),
          image_tags,
          image.id,
          image.location,
          image.ownerId, image.state, image.is_public, image.product_codes, image.architecture, image.type, image.ramdisk_id, image.kernel_id
        )
    r = "[%s]" % image_json_string[0:-2]
    return r
  
  def getInstanceList(self, req) :
    euca = None
    try :
      euca = Euca2ool()
    except Exception, e:
      print e
    
    euca_conn = euca.make_connection()
    try :
      reservations = euca_conn.get_all_instances()
    except Exception, ex:
      logging.error('cloud.py (86)' + ex)
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
      return_json_str = "[%s]" % instance_json_string[0:-2]
    a = simplejson.loads(return_json_str)
    return simplejson.dumps(a)
  
  def getRunningInstancesTree(self, req):
    
    euca = None
    try :
      euca = Euca2ool()
    except Exception, e:
      print e
    
    euca_conn = euca.make_connection()
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
    return return_json_str
  
  def launchInstance(self, req) :
    logging.error("_seungjin_ launch call")
    if req.method == "POST":
      #print req.POST
      #print req.POST['image_id']
      
      #req.POST['instance_name']
      #req.POST['instance_description']
      #req.POST['instance_tags']
      
      image_id = req.POST['image_id']
      keyname = req.POST['auth_key']
      kernel_id = None
      ramdisk_id = None
      min_count = req.POST['num_of_instances']
      max_count = req.POST['num_of_instances']
      instance_type = req.POST['instance_size']
      group_names = [ ]
      user_data = None
      user_data_file = None
      addressing_type = None
      zone = None
      try :
        euca = Euca2ool('k:n:t:g:d:f:z:',
          ['key=', 'kernel=', 'ramdisk=', 'instance-count=', 'instance-type=', 'group=', 'user-data=', 'user-data-file=', 'addressing=', 'availability-zone='])
      except Exception, e:
        logging.error("euca tool error: "+e)
      euca_conn = euca.make_connection()
      try :
        reservation = euca_conn.run_instances (
          image_id = image_id,
          min_count = min_count,
          max_count = max_count,
          key_name = keyname,
          security_groups = group_names,
          user_data = user_data,
          addressing_type = addressing_type,
          instance_type = instance_type,
          placement = zone,
          kernel_id = kernel_id,
          ramdisk_id = ramdisk_id
        )
      except Exception, e:
        logging.error("cloud error 272")
      
      for group in reservation.groups:
        for instance in reservation.instances:
          inst = Instances(
            instance_name = req.POST['instance_name'],
            instance_description = req.POST['instance_description'],
            instance_tags = req.POST['instance_tags'],
            reservation = reservation.id ,
            owner_id = reservation.owner_id,
            group_id = group.id,
            instance_id = instance.id ,
            machine_image = instance.image_id,
            public_dns_name = instance.public_dns_name,
            private_dns_name = instance.private_dns_name,
            state = instance.state,
            ami_index = instance.ami_launch_index,
            product_code = instance.product_codes,
            machine_size = instance.instance_type,
            placement = instance.placement,
            key_name = instance.key_name,
            launch_time = instance.launch_time,
            kernel = instance.kernel,
            ramdisk = instance.ramdisk
          )
          inst.save()
      
      
      #return """[{"instance_id" : "%s"}]""" % reservation
      #reservation = euca_conn.run_instances(image_id=req.POST['image_id'],key_name='seungjin')
      return """[{"instance_id" : "1"}]"""
  
  def terminateInstance(self, req) :
    if req.method == "POST" :
      euca = Euca2ool()
      euca_conn = euca.make_connection()
      instance_ids = []
      instance_ids.append(req.POST['instance_id'])
      print instance_ids
      try :
        euca_conn.terminate_instances(instance_ids)
      except Exception, ex:
        print ex
      
      # update status in my db
      try:
        e = Instances.objects.get(instance_id = req.POST['instance_id'])
        e.state = 'terminated'
        e.save()
      except : 
        pass
  
  def getKeyPairsList(self, req) :
    euca = Euca2ool()
    euca_conn = euca.make_connection()
    keypairs = euca_conn.get_all_key_pairs()
    keypairs_list = ''
    for keypair in keypairs :
      keypair_string = """{'keypair_name' : '%s', 'keypair_fingerprint' : '%s'},""" % (keypair.name, keypair.fingerprint)
      keypairs_list = keypairs_list + keypair_string
    return "[%s]" % keypairs_list[0:-1]
  
  def getKeyPairsListTree(self, req) :
    euca = Euca2ool()
    euca_conn = euca.make_connection()
    keypairs = euca_conn.get_all_key_pairs()
    keypairs_list = ''
    keypair_id = 0
    for keypair in keypairs :
      keypair_id = keypair_id + 1
      keypair_string = """{'id' : '%s', 'text' : '%s', 'leaf' : 'false'},""" % (keypair_id,keypair.name)
      keypairs_list = keypairs_list + keypair_string
    return "[%s]" % keypairs_list[0:-1]
  
  def createKeyPair(self, req) :
    euca = Euca2ool()
    euca_conn = euca.make_connection()
    keypair = euca_conn.create_key_pair(req.POST['keypair_name'])
    print keypair.material
  
  def removeKeyPair(self, req) :
    pass
  
  def getVolumeListTree(self, reg) :
    logging.debug("_seungjin_ getVolumeListTree called")
    euca = Euca2ool()
    euca_conn = euca.make_connection()
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
    return "["+volume_json_string[0:-2]+"]"
  
  def getMachineImageTree(self,req):
    euca = Euca2ool()
    image_ids = euca.process_args()
    image_json_string = ""
    euca_conn = euca.make_connection()
    images = euca_conn.get_all_images()
    image_no = 0
    for image in images :
      if image.type == "machine" :
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
    return r

  def getVolumeList(self,req) :
    logging.debug("_seungjin_ method call : getVolumeList")
    euca = Euca2ool()
    euca_conn = euca.make_connection()
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
    logging.debug("_seungjin_ 2" + "["+volume_json_string[0:-2]+"]")
    return "["+volume_json_string[0:-2]+"]"
  
  def attachVolume(self,req) :
    if req.method == "POST":
      instance_id = req.POST['instance_id']
      device = req.POST['device']
      volume_id = req.POST['volume_id']
      try:
        euca = Euca2ool('i:d:', ['instance=', 'device='])
      except Exception, e:
        print e
      euca_conn = euca.make_connection()
      try:
        return_code = euca_conn.attach_volume(volume_id = volume_id, instance_id = instance_id, device = device)
      except Exception, ex:
        logging.error(ex)
      return return_code
  
  def detachVolume(self,req) :
    if req.method == "POST":
      instance_id = req.POST['instance_id']
      volume_id = req.POST['volume_id']
      try:
        euca = Euca2ool('i:d:', ['instance=', 'device='])
      except Exception, e:
        print e
      euca_conn = euca.make_connection()
      try:
        return_code = euca_conn.detach_volume(volume_id = volume_id)
      except Exception, ex:
        logging.error(ex)
      return return_code

  def getVmTypes(self,req) :
    reString = """[
      {"name" : "m1.small" , "cpus" : "1" , "memory" : "128" , "disc" : "2"},
      {"name" : "c1.medium" , "cpus" : "1" , "memory" : "256" , "disc" : "5"},
      {"name" : "m1.large" , "cpus" : "2" , "memory" : "512" , "disc" : "10"},
      {"name" : "m1.xlarge" , "cpus" : "2" , "memory" : "1024" , "disc" : "20"},
      {"name" : "c1.xlarge" , "cpus" : "4" , "memory" : "2048" , "disc" : "20"}
    ]"""
    return reString
  
  def getInstanceInfo(self,req) :
    euca = None
    try :
      euca = Euca2ool()
    except Exception, e:
      logging.error(e)
    
    euca_conn = euca.make_connection()
    instance_id_list = []
    instance_id_list.append(req.GET['instance_id'])
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
            instance_image_name = ""
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
    return simplejson.dumps(a)

  def getAttachedVolumeList(self,req) :
    euca = Euca2ool()
    euca_conn = euca.make_connection()
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
    return "["+volume_json_string[0:-2]+"]"


# usage
#test = Cloud(ec2_access_key='4iNIDXPptlD20Ywnh8Gu9fKdrJLhoDUSX8ibHg',ec2_secret_key='QiYbTUsoLmMQKCnKHUFBIQ27U7dOl3kbI0SDaA')
#test.getKeyPairsList()
