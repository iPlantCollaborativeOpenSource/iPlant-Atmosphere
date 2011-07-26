


from atmosphere.cloudservice.models import * 

from atmosphere.cloudservice.lib.Amazon_model_template import *
from atmosphere.cloudservice.lib.Openstack_model_template import *
from atmosphere.cloudservice.lib.Eucalyptus_model_template import *


import json

import gevent

"""

resource json example:

{"resource_name":"my eucalyptus 1", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}
{"resource_name":"my eucalyptus 2", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}

{"resource_name":"my aws 1", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}
{"resource_name":"my aws 2", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}

{"resource_name":"my openstack 1", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}
{"resource_name":"my openstack 2", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}

"""

class Mycloud(object):

  def __init__(self,userid):
    """
    debug sample data
    """
    #debug_resource_1_json = """{"resource_name":"my eucalyptus 1", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
    #debug_resource_2_json = """{"resource_name":"my eucalyptus 2", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
    #debug_resource_3_json = """{"resource_name":"my aws 1", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
    #debug_resource_4_json = """{"resource_name":"my aws 2", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
    #debug_resource_5_json = """{"resource_name":"my openstack 1", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
    #debug_resource_6_json = """{"resource_name":"my openstack 2", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""

    #self.resource_list = []
    #self.resource_list.append(json.loads(debug_resource_1_json))
    #self.resource_list.append(json.loads(debug_resource_2_json))
    #self.resource_list.append(json.loads(debug_resource_3_json))
    #self.resource_list.append(json.loads(debug_resource_4_json))
    #self.resource_list.append(json.loads(debug_resource_5_json))
    #self.resource_list.append(json.loads(debug_resource_6_json))
    """
    end of debug sample data
    """
    resources = Cloud_resources.objects.filter(username = userid)
    self.resource_objects_list = []

    for resource in resources:
      if json.loads(resource.getResourceJson())['resource_type'] == "eucalyptus" :
        #print json.loads(resource.getResourceJson())['resource_information']
        #print json.loads(resource.getResourceJson())['resource_information']['quota']
        self.resource_objects_list.append(Eucalyptus_model_template(
          access_key = json.loads(resource.getResourceJson())['resource_information']['access_key'],
          access_secret = json.loads(resource.getResourceJson())['resource_information']['secret_key'], 
          ec2_url = json.loads(resource.getResourceJson())['resource_information']['ec2_url'],
          s3_url = json.loads(resource.getResourceJson())['resource_information']['s3_url'], 
          quota_option = json.loads(resource.getResourceJson())['resource_information']['quota']
        ))
      if json.loads(resource.getResourceJson())['resource_type'] == "amazon" :
        self.resource_objects_list.append(Amazon_model_template(
          access_key = json.loads(resource.getResourceJson())['resource_information']['access_key'],
          access_secret = json.loads(resource.getResourceJson())['resource_information']['secret_key'],
          quota_option = json.loads(resource.getResourceJson())['resource_information']['quota']
        ))
        pass
      if json.loads(resource.getResourceJson())['resource_type'] == "openstack" :
        pass

  def get_all_images(self):
    # I want to do this part with asynchnous programming!
    for resource in self.resource_objects_list :
      print resource.get_all_images()
  
  def get_all_instances(self):
    # I want to do this part with asynchnous programming!
    for resource in self.resource_objects_list :
      print resource.get_all_instances()

  def launch_instance(self):
    pass
  
  def get_regions(self):
    for resource in self.resource_objects_list : 
      print resource.get_regions()



#debug_resource_1_json = """{"resource_name":"my eucalyptus 1", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#debug_resource_2_json = """{"resource_name":"my eucalyptus 2", "resource_type":"eucalyptus", "resource_information":{"access_key":"apple","secret_key":"","ec2_url":"","s3_url":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#debug_resource_3_json = """{"resource_name":"my aws 1", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#debug_resource_4_json = """{"resource_name":"my aws 2", "resource_type":"aws", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#debug_resource_5_json = """{"resource_name":"my openstack 1", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#debug_resource_6_json = """{"resource_name":"my openstack 2", "resource_type":"openstack", "resource_information":{"access_key":"", "secret_key":"", "quota":{"core":2,"memory":2048,"storage":10,"max_instance":2,"max_vm_resource_life":100}}}"""
#
#debug_purpose_cloud_resource_list = [json.loads(debug_resource_1_json), json.loads(debug_resource_2_json), json.loads(debug_resource_3_json), json.loads(debug_resource_4_json), json.loads(debug_resource_5_json), json.loads(debug_resource_6_json)] 





#a = Mycloud("seungjin")

#a.load_amazon_model_resources()
#print a.resource_objects_list[0].a


