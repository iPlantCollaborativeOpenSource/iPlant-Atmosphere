


import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

from urlparse import urlparse


class Eucalyptus_model_template():
  """When boto implementation works perfectly with eucalyptus, this should/can be get rid of"""
  def __init__(self, access_key, access_secret, ec2_url, s3_url, quota_option=None):
    self.access_key = access_key
    self.access_secret = access_secret
    self.ec2_url = ec2_url
    self.s3_url = s3_url
    self.quota = quota_option
    self.region = RegionInfo(name="eucalyptus", endpoint=urlparse(self.ec2_url).netloc.split(":")[0])

    print self.access_key
    print self.access_secret
    print self.region

    self.connection = boto.connect_ec2(
                  aws_access_key_id=str(self.access_key),
                  aws_secret_access_key=str(self.access_secret),
                  is_secure=False,
                  region=self.region,
                  port=int(urlparse(self.ec2_url).netloc.split(":")[1]),
                  path="/services/Eucalyptus")
  
  def getAllImages(self):
    images = self.connection.get_all_images()
    print images

