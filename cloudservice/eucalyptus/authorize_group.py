#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#



from datetime import datetime

import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from boto.utils import get_instance_metadata
from boto.ec2.securitygroup import SecurityGroup
from atmosphere.cloudservice.models import *


def open_port(user,port):
  if user == "*":
    users = Ec2_keys.objects.filter()
    user_list = []
    for user in users:
      user_list.append(user.username)
  else :
    user_list = user.split(",")


def open_ping(user):
  if user == "*":
    users = Ec2_keys.objects.filter()
    user_list = [];
    for user in users:
      user_list.append(user.username)
  else :
    user_list = user.split(",")
  
  for user in user_list:
    
    #http://boto.s3.amazonaws.com/ref/ec2.html#module-boto.ec2.securitygroup
    #class boto.ec2.securitygroup.SecurityGroup(connection=None, owner_id=None, name=None, description=None)
    #authorize(ip_protocol=None, from_port=None, to_port=None, cidr_ip=None, src_group=None)
    # Add a new rule to this security group. You need to pass in either src_group_name OR ip_protocol, from_port, to_port, and cidr_ip. In other words, either you are authorizing another group or you are authorizing some ip-based rule.
    #
    # Parameters: 
    #   ip_protocol (string) – Either tcp | udp | icmp
    #   from_port (int) – The beginning port number you are enabling
    #   to_port – The ending port number you are enabling
    #   to_port (string) – The CIDR block you are providing access to. See http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
    #   Return type:  bool
    #   Returns:  True if successful.


    ec2_key = Ec2_key.objects.get(username = user).ec2_access_key
    ec2_secret = Ec2_key.objects.get(username = user).ec2_secret_key
    ec2_url = Ec2_key.objects.get(username = user).ec2_url
    region = RegionInfo(name="eucalyptus", endpoint=urlparse(ec2_url).netloc.split(":")[0])
    connection = boto.connect_ec2(aws_access_key_id=str(ec2_key),
                  aws_secret_access_key=str(ec2_secret),
                                is_secure=False,
                                region=region,
                                port=8773,
                                path="/services/Eucalyptus")
    #volumes = connection.get_all_volumes(owner="edwintest")
    #sg = SecurityGroup(connection,owner_id=)
    
  
