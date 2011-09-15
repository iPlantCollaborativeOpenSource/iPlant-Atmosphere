#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


from datetime import datetime
from datetime import timedelta


import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo


from atmosphere.cloudservice.models import *
from urlparse import urlparse
from django.utils import simplejson
import atmosphere.cloudservice.api.v1.util as atmo_util

from datetime import timedelta

import inspect

from django.core.mail import send_mail
from string import Template

def send_termination_notification_mail(instance_id):
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
  instance = Instances.objects.get(instance_id = instance_id)
  instance_name = instance.instance_name
  instance_description = instance.instance_description
  instance_tags = instance.instance_tags
  instance_reservation = instance.reservation
  instance_owner_id = instance.owner_id
  instance_group_id = instance.group_id
  instance_instance_id = instance.instance_id
  instance_machine_image = instance.machine_image
  instance_public_dns_name = instance.public_dns_name
  instance_private_dns_name = instance.private_dns_name
  instance_key_name = instance.key_name
  instance_current_state = instance.current_state
  instance_ami_index = instance.ami_index
  instance_product_code = instance.product_code
  instance_machine_size = instance.machine_size
  instance_launch_time = instance.launch_time
  instance_placement = instance.placement
  instance_kernel = instance.kernel
  instance_ramdisk = instance.ramdisk
  instance_launch_request_time = instance.launch_request_time
  instance_lifetime = instance.lifetime
  instance_launch_response_time = instance.launch_response_time
  instance_termination_request_time = instance.termination_request_time

  #import ldap
  #dn = 'ou=people,dc=iplantcollaborative,dc=org'
  #server = 'ldap://ldap.iplantcollaborative.org'
  #conn = ldap.initialize(server)
  #a = conn.search_s(dn, ldap.SCOPE_SUBTREE,'(uid='+userid+')',['mail'])
  #toemail = a[0][1]['mail'][0]
  #fromemail = Configs.objects.get(key="admin_email").value

  #instance_id = simplejson.loads(message)['instance-id']
  #ip = simplejson.loads(message)['public-ipv4']
  #username = simplejson.loads(message)['linuxusername']
  #msg =  'Your Atmosphere cloud instance is terminated.\n\nInstance id: %s\nIP: %s\nSSH Username: %s\nSSH Password: %s\n\nAtmosphere, iPlant Collaborative' % (instance_id, ip, username, password)
  #send_mail('Your Atmosphere Cloud Instance Ternimated', msg, fromemail, [toemail], fail_silently=False)

  email_notification_template = Email_notification_templates.objects.get(name='default instance termination email')
  email_replay_to = email_notification_template.reply_to
  
  email_subject_template = Template(email_notification_template.subject)
  email_subject = email_subject_template.substitute( current_time=current_time,
                            instance_name=instance_name,
                            instance_description=instance_description,
                            instance_tags = instance_tags,
                            instance_reservation = instance_reservation,
                            instance_owner_id = instance_owner_id,
                            instance_group_id = instance_group_id,
                            instance_id = instance_instance_id,
                            instance_machine_image = instance_machine_image,
                            instance_public_dns_name = instance_public_dns_name,
                            instance_private_dns_name = instance_private_dns_name,
                            instance_key_name = instance_key_name,
                            instance_current_state = instance_current_state,
                            instance_ami_index = instance_ami_index,
                            instance_product_code = instance_product_code,
                            instance_machine_size = instance_machine_size,
                            instance_launch_time = instance_launch_time,
                            instance_placement = instance_placement,
                            instance_kernel = instance_kernel,
                            instance_ramdisk = instance.ramdisk,
                            instance_launch_request_time = instance_launch_request_time,
                            instance_lifetime = instance_lifetime,
                            instance_launch_response_time = instance_launch_response_time,
                            instance_termination_request_time = instance_termination_request_time
                          )
  email_body_template = Template(email_notification_template.body)
  email_body = email_body_template.substitute( current_time=current_time,
                            instance_name=instance_name,
                            instance_description=instance_description,
                            instance_tags = instance_tags,
                            instance_reservation = instance_reservation,
                            instance_owner_id = instance_owner_id,
                            instance_group_id = instance_group_id,
                            instance_id = instance_instance_id,
                            instance_machine_image = instance_machine_image,
                            instance_public_dns_name = instance_public_dns_name,
                            instance_private_dns_name = instance_private_dns_name,
                            instance_key_name = instance_key_name,
                            instance_current_state = instance_current_state,
                            instance_ami_index = instance_ami_index,
                            instance_product_code = instance_product_code,
                            instance_machine_size = instance_machine_size,
                            instance_launch_time = instance_launch_time,
                            instance_placement = instance_placement,
                            instance_kernel = instance_kernel,
                            instance_ramdisk = instance.ramdisk,
                            instance_launch_request_time = instance_launch_request_time,
                            instance_lifetime = instance_lifetime,
                            instance_launch_response_time = instance_launch_response_time,
                            instance_termination_request_time = instance_termination_request_time
                          )
  #from_mail = Configs.objects.get('admin_email').value
  import ldap
  #dn = 'ou=people,dc=iplantcollaborative,dc=org' #should be database driven
  #server = 'ldap://ldap.iplantcollaborative.org' #should be database driven
  dn = Configs.objects.get(key='ldap_server_dn').value
  server = Configs.objects.get(key='ldap_server').value
  conn = ldap.initialize(server)
  a = conn.search_s(dn, ldap.SCOPE_SUBTREE,'(uid='+instance_owner_id+')',['mail']) 
  to_email = a[0][1]['mail'][0] #should be database driven
  from_email = Configs.objects.get(key="admin_email").value 
  send_mail(email_subject, email_body, from_email, [to_email], fail_silently=False)
