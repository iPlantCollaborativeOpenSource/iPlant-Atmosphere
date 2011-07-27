#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden

from django.utils import simplejson
import logging

from atmosphere.cloudauth.models import *
from atmosphere.cloudservice.models import *
from atmosphere.cloudservice.api.v1.cloud import *

from boto.exception import *


import httplib
import urllib
from urlparse import urlparse

import string

import datetime
from datetime import datetime
# /home/atmosphere_dev/atmosphere/cloudservice/api/v1/instanceservice.py:41: DeprecationWarning: The popen2 module is deprecated.  Use the subprocess module.
#import popen2
import subprocess

from django.utils import simplejson
from django.core.mail import send_mail

from string import Template

def sendPasswordEmail(userid,message):
  #user = simplejson.loads(message)['public-ipv4']
  import ldap
  #dn = 'ou=people,dc=iplantcollaborative,dc=org' #should be database driven
  #server = 'ldap://ldap.iplantcollaborative.org' #should be database driven
  dn = Configs.objects.get(key='ldap_server_dn').value
  server = Configs.objects.get(key='api_server_url').value
  conn = ldap.initialize(server)
  a = conn.search_s(dn, ldap.SCOPE_SUBTREE,'(uid='+userid+')',['mail']) 
  toemail = a[0][1]['mail'][0] #should be database driven
  fromemail = Configs.objects.get(key="admin_email").value 

  instance_id = simplejson.loads(message)['instance-id']
  ip = simplejson.loads(message)['public-ipv4']
  username = simplejson.loads(message)['linuxusername']
  password = simplejson.loads(message)['linuxuserpassword']
  vncpassword = simplejson.loads(message)['linuxuservncpassword']
  if vncpassword == None :
  	msg =  'Your Atmosphere cloud instance is ready.\n\nInstance id: %s\nIP: %s\nSSH Username: %s\nSSH Password: %s\n\nAtmosphere, iPlant Collaborative' % (instance_id, ip, username, password)
  else :
  	msg =  'Your Atmosphere cloud instance is ready.\n\nInstance id: %s\nIP: %s\nSSH Username: %s\nSSH Password: %s\nVnc Passoword: %s\n\nAtmosphere, iPlant Collaborative' % (instance_id, ip, username, password, vncpassword)
  send_mail('Your Atmosphere Cloud Instance', msg, fromemail, [toemail], fail_silently=False)

def emailNotification(message):
  instance_id = simplejson.loads(message)['instance-id']
  userid = simplejson.loads(message)['linuxusername']
  #
  # debug shell
  #from atmosphere.cloudservice.api.v1.instanceservice import emailNotification
  #msg = """{"linuxuservncpassword":null,"ami-id":"emi-D9602AB9","instance-type":"m1.small","block-device-mapping/swap":"sda3","block-device-mapping/ephemeral0":"sda2","public-hostname":"128.196.142.118","ami-manifest-path":"http://128.196.172.138:8773/services/Walrus/admin_mi_basic_xwindows_realvnc_ldap_20110525/admin_mi_basic_xwindows_realvnc_ldap_20110525.img.manifest.xml","placement/availability-zone":"bespin","ramdisk-id":"eri-B6B91781","block-device-mapping/emi":"sda1","linuxusername":"seungjin","local-hostname":"172.17.5.5","ancestor-ami-ids":"","linuxuserpassword":"","kernel-id":"eki-DB23180A","public-keys/0/openssh-key":"","public-keys/0=":"","block-device-mapping/root":"/dev/sda1","security-groups":"default","local-ipv4":"172.17.5.5","instance-id":"i-520F082A","product-codes":"","hostname":"128.196.142.118","ami-launch-index":"0","event_type":"instance_lunched","public-ipv4":"128.196.142.118","block-device-mapping/ephemeral":"sda2","reservation-id":"r-36CF0770"}"""
  #emailNotification(msg)
  #
  #
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
  instance = Instances.objects.get(instance_id = instance_id)
  #userid = instance.owner_id
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

  email_notification_template = Email_notification_templates.objects.get(name='default instance launch email')
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
                            instance_termination_request_time = instance_termination_request_time,
                            instance_username = userid
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
                            instance_termination_request_time = instance_termination_request_time,
                            instance_username = userid
                          )
  import ldap
  #dn = 'ou=people,dc=iplantcollaborative,dc=org' #should be database driven
  #server = 'ldap://ldap.iplantcollaborative.org' #should be database drive
  dn = Configs.objects.get(key='ldap_server_dn').value
  #server = Configs.objects.get(key='api_server_url').value
  server = Configs.objects.get(key='ldap_server').value
  conn = ldap.initialize(server)
  a = conn.search_s(dn, ldap.SCOPE_SUBTREE,'(uid='+instance_owner_id+')',['mail']) 
  to_email = a[0][1]['mail'][0]
  logging.debug(to_email)
  from_email = Configs.objects.get(key="admin_email").value 
  logging.debug(from_email)
  send_mail(email_subject, email_body, from_email, [to_email], fail_silently=False)

def sendWebhookCall(userid, message):
  #
  #logging.debug(":-) msg:" + message)
  #send_mail('debug',message,"seungjin@email.arizona.edu",["seungjin@email.arizona.edu"], fail_silently=False)
  #webhook_resource = "https://www.seungjin.net"
  webhook_resource = Instance_launch_hooks.objects.get(owner_id=userid, instance_id = simplejson.loads(message)['instance-id']).webhook_url
  o = urlparse(webhook_resource)
  webhook_server_url = string.split(o.netloc,":")[0]
  webhook_server_port = o.port
  webhook_server_path = o.path
  method = "POST"
  params = None
  headers = {
    "Content-type" : "application/x-www-form-urlencoded",
    "Accept" : "text/plain",
    "User-Agent" : "Atmosphere",
    "X-Atmo-Instance-Info" : message
  }
  if o.scheme == 'https' :
    conn = httplib.HTTPSConnection(webhook_server_url,webhook_server_port)
  elif o.scheme == 'http' :
    conn = httplib.HTTPConnection(webhook_server_url,webhook_server_port)
  conn.request(method,webhook_server_path,params,headers)
  r1 = conn.getresponse()
  Instance_launch_hooks.objects.filter(instance_id=simplejson.loads(message)['instance-id'], owner_id = userid).update(
    webhook_header_params = message,
    responsed_time = datetime.datetime.now(),
    responsed_header = str(r1.getheaders()),
    responsed_body = (r1.read())
  )

def update_cloudservice_instance_lifecycles_table(msg) :
  #logging.debug("update_cloudservice_instance_lifecycles_table")
  instance_id = simplejson.loads(msg)['instance-id']
  #logging.debug("update_cloudservice_instance_lifecycles_table: " + instance_id)
  instance_lifecycle_instance = Instance_lifecycles.objects.get(instance_id = instance_id)
  instance_lifecycle_instance.instance_launched_at = datetime.now()
  #logging.debug("update_cloudservice_instance_lifecycles_table: " + str(datetime.now()))
  instance_lifecycle_instance.save()

def call(request) :
  if request.method == "POST":
    token = request.POST['token']
    channel = request.POST['userid']
    message = request.POST['vminfo']
    #ami_index = request.POST['ami_index']
    ami_index = simplejson.loads(message)['ami-launch-index']
    instance = Instances.objects.get(instance_token=token,ami_index=ami_index)

    instanceservice_messages = Instanceservice_messages(token=token,channel=channel,message=message,ami_index=ami_index,instance=instance)
    instanceservice_messages.save()
    
    if instance.launch_response_time == None  :
      instance.current_state = "running"
      instance.launch_response_time = datetime.now()
      instance.public_dns_name = simplejson.loads(message)['public-ipv4']
      instance.private_dns_name = simplejson.loads(message)['local-ipv4']
      instance.save()
      node_path = Configs.objects.get(key="node_path").value
      sayjs_path = Configs.objects.get(key="say.js_path").value
      if simplejson.loads(message)['event_type'] == "instance_lunched" :
        #sendPasswordEmail(simplejson.loads(message)['public-ipv4'],simplejson.loads(message)['linuxusername'], simplejson.loads(message)['linuxuserpassword'])
        update_cloudservice_instance_lifecycles_table(message)
        #sendPasswordEmail(channel,message)
        emailNotification(message)

        notice_msg = "instance %s was launched with ip %s" % ( simplejson.loads(message)['instance-id'] , simplejson.loads(message)['public-ipv4'] )
        #run_cmd = lambda c : subprocess.Popen(c.split(None,3), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False).stdout.read()
        run_cmd = lambda c,a : subprocess.Popen(c.split(None,a), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False).stdout.read()
        cmd = '%s %s %s "%s"' % (node_path, sayjs_path, channel, notice_msg)
        run_cmd(cmd,3)
        #r, w, e = popen2.popen3('%s %s %s "%s"' % (node_path, sayjs_path, channel, notice_msg))
        #logging.debug(e.readlines())
        #logging.debug(r.readlines())
        #r.close()
        #e.close()
        #w.close()

        sendWebhookCall(channel,message)
      return HttpResponse("ok")
    else :
      return HttpResponse("launch_response_time is not null")
  else :
    return HttpResponse("invalid protocol")