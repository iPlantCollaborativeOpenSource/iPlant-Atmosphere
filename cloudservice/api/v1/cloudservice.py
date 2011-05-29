#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


from atmosphere.cloudservice.api.v1.cloud import Ec2_cloud
from atmosphere.cloudservice.api.v1.image import Image

class Cloudservice(Ec2_cloud, Image):
  
  def __init__():
    pass
  
  def jsoner(self,code,meta,value):
    final_json = """{
    "result" : {
        "code" : %s ,
        "meta" : %s ,
        "value" : %s
    } 
    }""" % (code,meta,value)
    return final_json
