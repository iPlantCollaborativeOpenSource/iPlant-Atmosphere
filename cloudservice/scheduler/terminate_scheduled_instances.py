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

def send_termination_notification_mail(instance_id):
  instance = Instances.objects.get(instance_id = instance_id)
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
  send_mail('Your Atmosphere Cloud Instance Ternimated', 'instance_terminated', 'seungjin@email.arizona.edu', ['seungjin@email.arizona.edu'], fail_silently=False)

def terminate_scheduled_instances():
  # read cloudservice_instance_lifecyels table
  instance_lifecycles = Instance_lifecycles.objects.filter(instance_terminated_at = None, instance_lifetime_extended_at = None).exclude(instance_launched_at = None)
  for instance in instance_lifecycles:
    if instance.instance_lifetime > 0 :
      instance_end_time = instance.instance_launched_at + timedelta(hours=instance_lifecycles[0].instance_lifetime) + timedelta(minutes=1)
      #print (datetime.now() - instance_end_time).days
      if ((datetime.now() - instance_end_time).days) >= 0 :
        ec2_key = Configs.objects.get(key = "admin_ec2_access_key").value
        ec2_secret = Configs.objects.get(key = "admin_ec2_secret_key").value
        ec2_url = Configs.objects.get(key = "admin_ec2_url").value
        current_time = datetime.now()
        region = RegionInfo(name="eucalyptus", endpoint=urlparse(ec2_url).netloc.split(":")[0])
        connection = boto.connect_ec2(aws_access_key_id=str(ec2_key), aws_secret_access_key=str(ec2_secret), is_secure=False, region=region, port=8773, path="/services/Eucalyptus")
        connection.terminate_instances([instance.instance_id])
        terminated_instance = Instance_lifecycles.objects.get(instance_id = instance.instance_id)
        terminated_instance.instance_terminated_at = current_time
        terminated_instance.instance_terminated_by = inspect.stack()[0][3]
        terminated_instance.save()
        instance = Instances.objects.get(instance_id = instance.instance_id)
        instance.termination_request_time = current_time
        instance.save()

        send_termination_notification_mail(instance.instance_id)
        # let's send notification email
        print "!~~~~~~~!"