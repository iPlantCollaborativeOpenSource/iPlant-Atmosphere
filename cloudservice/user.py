#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from atmosphere.cloudservice.models import *

class User(object) :
  """
    User object
  """
  
  user_name = None
  user_token = None
  user_api_server_url = None 
  user_ec2_access_key = None
  user_ec2_secret_key = None
  
  def __init__(self,username,token,api_server_url) :
    
    self.user_name = username
    self.user_token= token
    self.user_api_server_url = api_server_url
    
    ec2_key = Ec2_keys
    user_info = ec2_key.objects.get(username=username)
    self.user_ec2_access_key = user_info.ec2_access_key
    self.user_ec2_secret_key = user_info.ec2_secret_key


class Image(Object) :
  
  def getImageList(self, req):
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
  
  
