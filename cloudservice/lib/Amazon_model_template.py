


from boto.ec2.connection import EC2Connection
import boto.ec2

class Amazon_model_template():
  """ this covers amazon aws"""
  def __init__(self, ec2_key, ec2_secret):
    self.access_key = ec2_key
    self.access_secret = ec2_secret
    self.conn = EC2Connection(self.access_key, self.access_secret)
    self.regions = boto.ec2.regions()
    
	
  