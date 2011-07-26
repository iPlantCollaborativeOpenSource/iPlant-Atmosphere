


from boto.ec2.connection import EC2Connection
import boto.ec2

class Amazon_model_template():
  """ this covers amazon aws"""
  def __init__(self, access_key, access_secret, quota_option=None):
    self.access_key = access_key
    self.access_secret = access_secret
    self.quota = quota_option
    self.connection = EC2Connection(aws_access_key_id=str(self.access_key),aws_secret_access_key=str(self.access_secret))
  
  def get_all_images(self):
    for image in self.connection.get_all_images() :
      print "arhcitecture: " + str(image.architecture)
      print "description: " + str(image.description)
      print "get_kernel: " + str(image.get_kernel)
      print "launch_permission: " + str(image.get_launch_permissions)
      print "get_ramdisk: " + str(image.get_ramdisk)
      print "id: " + str(image.id)
      print "is_public: " + str(image.is_public)
      print "item: " + str(image.item)
      print "kernel_id: " + str(image.kernel_id)
      print "location: " + str(image.location)
      print "name: " + str(image.name)
      print "owner_id: " + str(image.ownerId)
      print "owner_alias: " + str(image.owner_alias)
      print "platform: " + str(image.platform)
      print "product_codes: " + str(image.product_codes)
      print "ramdisk_id: " + str(image.ramdisk_id)
      print "region: " + str(image.region)
      print "root_device_name: " + str(image.root_device_name)
      print "device_type: " + str(image.root_device_type)
      print "state: " + str(image.state)
      print "type: " + str(image.type)
      print "<<<<<<"
    
  
  def get_all_instances(self):
    reservations = self.connection.get_all_instances()
    for reservation in reservations:
      for instance in reservation.instances:
        print instance
        print instance.dns_name
        print instance.public_dns_name
        print instance.state
    
  def get_regions(self):
    print self.connection.region

  def get_all_security_groups():
    pass
  
