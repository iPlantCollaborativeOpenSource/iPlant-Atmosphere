


from boto.ec2.connection import EC2Connection
import boto.ec2

class Amazon_model_template():
  """ this covers amazon aws"""
  def __init__(self, access_key, access_secret, quota_option=None):
    self.access_key = access_key
    self.access_secret = access_secret
    self.quota = quota_option
    self.connection = EC2Connection(aws_access_key_id=str(self.access_key),aws_secret_access_key=str(self.access_secret))
  
  def getAllImages(self):
    images = self.connection.get_all_images()
    print images
  
  def getAllInstances(self):
    instances = self.connection.get_all_instances()
    print instances
    
	
  