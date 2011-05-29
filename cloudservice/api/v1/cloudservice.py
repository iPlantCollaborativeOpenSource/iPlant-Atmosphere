

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