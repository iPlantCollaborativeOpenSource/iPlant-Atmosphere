# -*- coding: utf-8 -*- 
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from django.db import models
from django.utils.encoding import smart_str, smart_unicode




from time import strftime

#class UnixTimestampField(models.DateTimeField):
#  """UnixTimestampField: create a DateTimeField that is represented on the database as a TIMESTAMP field rather than the usual DATETIME field at MySQL"""
#
#  description = "UnixTimestampField for mysql"
#
#  __meta_class__ = models.SubfieldBase
#
#  def __init__(self, null=False, blank=False, **kargs):
#    super(UnixTimestampField, self).__init__(**keargs)
#    #default for TIMESTAMP is NOT NULL unlike most fields, so we have to cheat a litte
#    self.blank, self.isnull = blank, null 
#    self.null = True # To prevent the framework from shoving in "not null".
#
#  def db_type(self):
#    typ = ['TIMESTAMP']
#    # see above!
#    if self.isnull : 
#      typ += ['NULL']
#    if self.auto_created:
#      typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
#    return ' '.join(typ)
#  
#  def to_python(self, value):
#    return datetime.from_timestamp(value)
#  
#  def get_db_prep_value(self, value):
#    if value == None:
#      return None
#    return strftime('%Y%m%d%H%M%S',value.timetuple()) 

class TimestampField(models.Field):
  # reference: https://docs.djangoproject.com/en/dev/howto/custom-model-fields/
  def db_type(self, connection):
    if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
      #return 'datetime'
      return 'timestamp'
    else:
      return 'timestamp'

class TimeDecimalField(models.Field):
  def db_type(self, connection):
    return 'double(20,6)'
    

# Create your models here.

class Configs(models.Model):
  """ 
    system configuration / key-value pair
  """
  key = models.TextField()
  value = models.TextField()
  def __unicode__(self):
    return smart_str('%s %s' % (self.key, self.value))

class Ec2_keys(models.Model):
  """
    ec2_access_key, ec2_secret_key
  """
  username = models.CharField(max_length=256)
  ec2_access_key = models.TextField()
  ec2_secret_key = models.TextField()
  ec2_url = models.TextField()
  s3_url = models.TextField()
  added_at = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return smart_str('%s %s %s %s %s %s' % (self.username, self.ec2_access_key, self.ec2_secret_key, self.ec2_url, self.s3_url, self.added_at))







class Instances(models.Model):
  """
  instances database
  """
  # my info
  atmosphere_resource_id = models.CharField(max_length=255,null=True) 
  instance_name = models.CharField(max_length=128,null=True)
  instance_description = models.TextField(null=True)
  instance_tags = models.TextField(null=True)
  # information from euca
  reservation = models.CharField(max_length=128,null=True)
  owner_id = models.CharField(max_length=128,null=True)
  group_id = models.CharField(max_length=128,null=True)
  instance_id = models.CharField(unique=True,max_length=128,null=True)
  machine_image = models.CharField(max_length=128,null=True)
  public_dns_name = models.CharField(max_length=128,null=True)
  private_dns_name = models.CharField(max_length=128,null=True)
  key_name = models.CharField(max_length=128,null=True)
  current_state = models.CharField(max_length=128,null=True)
  ami_index = models.CharField(max_length=128,null=True)
  product_code = models.CharField(max_length=128,null=True)
  machine_size = models.CharField(max_length=128,null=True)
  launch_time = models.CharField(max_length=128,null=True) # get from eucalyptus as string
  placement = models.CharField(max_length=128,null=True)
  kernel = models.CharField(max_length=128,null=True)
  ramdisk = models.CharField(max_length=128,null=True)
  launch_request_time = models.DateTimeField(null=True)
  user_data = models.TextField(null=True)
  launched_by = models.CharField(max_length=128,null=True)
  launch_request_run_time = models.DateTimeField(null=True)
  launch_qued_num = models.IntegerField(null=True)
  #lifetime = models.IntegerField(null=True)
  lifetime = models.CharField(max_length=255,null=True)
  instance_token = models.CharField(max_length=128,null=True)
  launch_response_time = models.DateTimeField(null=True)
  termination_request_time =  models.DateTimeField(null=True)

  def time_took_for_launch(self):
    if (self.launch_response_time != None) and (self.launch_request_time != None) :
      return self.launch_response_time - self.launch_request_time
    else :
      return None

  def running_time(self):
    pass

class Resource_indexes(models.Model):
  """
  central resource management
  """
  resource_id = models.CharField(max_length=255)
  resource_type = models.CharField(max_length=255,null=True)
  resource_owner = models.CharField(max_length=255,null=True)
  resource_group = models.CharField(max_length=255,null=True)
  resource_created_at = models.DateTimeField(auto_now=True)
  resource_created_by = models.CharField(max_length=255,null=True)
  resource_deleted_at = models.DateTimeField(null=True)
  resource_deleted_by = models.CharField(max_length=255,null=True)

class Machine_images(models.Model):
  """
  null
  """
  # my info
  image_name = models.CharField(max_length=128, null=True)
  image_description = models.TextField(null=True)
  image_tags = models.TextField(null=True)
  image_application_stack_list = models.CharField(max_length=128, null=True)
  # euca info
  image_id = models.CharField(max_length=128,null=True)
  image_location = models.CharField(max_length=128,null=True)
  image_ownerid = models.CharField(max_length=128,null=True)
  image_state = models.CharField(max_length=128,null=True)
  image_type = models.CharField(max_length=128,null=True)
  image_ramdisk_id = models.CharField(max_length=128,null=True)
  image_kernel_id = models.CharField(max_length=128,null=True)
  image_is_public = models.CharField(max_length=128,null=True)
  image_product_code = models.CharField(max_length=128,null=True)
  image_architect = models.CharField(max_length=128,null=True)
  machine_image_user_data_scripts_script_id = models.CharField(max_length=128,null=True)
  registered_at = models.DateTimeField(null=True)

class Machine_volumes(models.Model):
  """
  null
  """
  # my info
  volume_name = models.CharField(max_length=128,null=True)
  volume_description = models.TextField(null=True)
  volume_tags = models.TextField(null=True)
  volume_owner = models.CharField(max_length=128,null=True)
  # euca info
  volume_id = models.CharField(unique=True,max_length=128,null=True)
  volume_size = models.CharField(max_length=128,null=True)
  volume_snapshot_id = models.CharField(unique=True,max_length=128,null=True)
  volume_status = models.CharField(max_length=128,null=True)
  volume_create_time = models.DateTimeField(null=True)
  volume_attach_data_instance_id = models.CharField(max_length=128,null=True)
  volume_attach_data_device = models.CharField(max_length=128,null=True)
  volume_attach_data_attach_time = models.DateTimeField(null=True)

class Api_logs(models.Model):
  """
  api log
  """
  request_user = models.CharField(max_length=128)
  request_token = models.CharField(max_length=128)
  request_remote_ip = models.CharField(max_length=64)
  request_remote_user_agent = models.CharField(max_length=128,null=True)
  request_url = models.TextField() 
  request_method = models.CharField(max_length=128)
  http_request_method = models.CharField(max_length=32)
  request_param = models.TextField(null=True)
  #request_time = models.DateTimeField() 
  #request_time = TimestampField(null=True)
  # SQL-92 stadnard, timestamp does not have millisecond. (postgresql does). So I use FloatField to record milliseconds.
  #request_time = models.FloatField(null=True)
  request_time = TimeDecimalField(null=True)
  response_value = models.TextField(null=True)
  #response_time = models.DateTimeField(null=True)
  #response_time = models.FloatField(null=True)
  response_time = TimeDecimalField(null=True)

class Applications(models.Model):
  """
  Applications (on-click launch)
  """
  application_name = models.CharField(max_length=128,null=True)
  application_icon_path = models.CharField(max_length=128,null=True)
  application_id = models.CharField(max_length=128,null=True)
  application_creator = models.CharField(max_length=128,null=True)
  application_created = models.DateTimeField(null=True)
  application_version = models.CharField(max_length=128,null=True)
  application_category = models.CharField(max_length=128,null=True)
  application_type = models.CharField(max_length=128,null=True)
  platform = models.CharField(max_length=128,null=True)
  machine_image_id = models.CharField(max_length=128,null=True)
  kernel_id = models.CharField(max_length=128,null=True)
  ramdisk_id = models.CharField(max_length=128,null=True)
  system_minimum_requirements = models.CharField(max_length=128,null=True)
  application_lifetime = models.IntegerField(null=True)
  application_tags = models.CharField(max_length=128,null=True)
  application_description = models.TextField(null=True)
  application_init_config_param = models.TextField(null=True)
  machine_image_user_data_scripts_script_id = models.CharField(max_length=128,null=True)

class User_applications(models.Model):
  """
  Applications (on-click launch)
  """
  user_id = models.CharField(max_length=128,null=True)
  application_id = models.CharField(max_length=128,null=True)
  application_name = models.CharField(max_length=128,null=True)
  application_icon_path = models.CharField(max_length=128,null=True)
  application_order = models.CharField(max_length=128,null=True)
  application_created = models.DateTimeField(null=True)
  application_version = models.CharField(max_length=128,null=True)
  application_category = models.CharField(max_length=128,null=True)
  application_type = models.CharField(max_length=128,null=True)
  platform = models.CharField(max_length=128,null=True)
  machine_image_id = models.CharField(max_length=128,null=True)
  kernel_id = models.CharField(max_length=128,null=True)
  ramdisk_id = models.CharField(max_length=128,null=True)
  system_minimum_requirements = models.CharField(max_length=128,null=True)
  application_lifetime = models.IntegerField(null=True)
  application_tags = models.CharField(max_length=128,null=True)
  application_description = models.TextField(null=True)
  application_init_config_param = models.TextField(null=True)
  machine_image_user_data_scripts_script_id = models.CharField(max_length=128,null=True)

class User_resource_quotas(models.Model):
  userid = models.CharField(max_length=128)
  cpu = models.IntegerField(null=True)
  memory = models.IntegerField(null=True)
  totoal_ebs_size = models.IntegerField(null=True)

class Machine_image_userdata_scripts(models.Model):
  script_id = models.IntegerField(unique=True) 
  script_name = models.CharField(max_length=128,null=True)
  script_description = models.TextField(null=True)
  script_version = models.CharField(max_length=128,null=True)
  script = models.TextField(null=True)
  updated_at = models.DateTimeField(null=True)
  def __unicode__(self):
    return smart_str('%s %s %s %s %s' % (self.script_id, self.script_name, self.script_description, self.script_version, self.script))

class Instance_launch_hooks(models.Model):
  instance_id = models.CharField(max_length=128,null=True)
  owner_id = models.CharField(max_length=128,null=True)
  webhook_url = models.CharField(max_length=128,null=True)
  webhook_header_params = models.TextField(null=True)
  requested_time = models.DateTimeField(null=True)
  responsed_time = models.DateTimeField(null=True)
  responsed_header = models.CharField(max_length=128,null=True)
  responsed_body = models.TextField(null=True)

class Resources_watches(models.Model):
  resource_name = models.CharField(max_length=255)
  resource_get_function_name = models.CharField(max_length=255)
  resource_get_function_result = models.TextField()
  updated_at = models.DateTimeField(auto_now_add=True)

class Instance_lifecycles(models.Model):
  atmosphere_resource_id = models.CharField(max_length=255,null=True)
  instance_id = models.CharField(max_length=128,null=True)
  instance_launched_at = models.DateTimeField(null=True)
  instance_lifetime = models.IntegerField(null=True)
  instance_terminated_at = models.DateTimeField(null=True)
  instance_terminated_by = models.CharField(max_length=128,null=True)
  instance_lifetime_extended_at = models.DateTimeField(null=True)

class Email_notification_templates(models.Model):
  name = models.CharField(max_length=255,null=True)
  description  = models.CharField(max_length=255,null=True)
  reply_to = models.CharField(max_length=255,null=True)
  subject = models.CharField(max_length=255,null=True)
  body = models.TextField(null=True)
  creator = models.CharField(max_length=128,null=True)
  created_at = models.DateTimeField(null=True)

class Cloud_resources(models.Model):
  """
    experimental, prototype, multi cloud resources table.
    sotring this kind of json: {"resource_name":"my eucalyptus 1", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}
  """
  username = models.CharField(max_length=255,null=False)
  resource_name = models.CharField(max_length=255,null=True)
  resource_type = models.CharField(max_length=255,null=True)
  resource_information = models.CharField(max_length=255,null=True)
  resource_quota = models.CharField(max_length=255,null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def getResourceJson(self):
    return """{"resource_name":"%s", "resource_type":"%s", "resource_information":{%s, "quota":{%s}}}""" % (self.resource_name, self.resource_type, self.resource_information, self.resource_quota)

class Instanceservice_messages(models.Model):
  token = models.CharField(max_length=255,null=True)
  channel = models.CharField(max_length=255,null=True)
  message = models.TextField()
  ami_index = models.CharField(max_length=255,null=True)
  instance = models.CharField(max_length=255,null=True)
  created_at = models.DateTimeField(auto_now_add=True)


