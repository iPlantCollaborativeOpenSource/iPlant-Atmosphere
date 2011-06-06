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

def sendPasswordEmail(userid,message):
  #user = simplejson.loads(message)['public-ipv4']
  import ldap
  dn = 'ou=people,dc=iplantcollaborative,dc=org'
  server = 'ldap://ldap.iplantcollaborative.org'
  conn = ldap.initialize(server)
  a = conn.search_s(dn, ldap.SCOPE_SUBTREE,'(uid='+userid+')',['mail'])
  toemail = a[0][1]['mail'][0]
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

def emailNotification(userid,message):
  """
  template based user email notification system
  """
  pass

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
  logging.debug("update_cloudservice_instance_lifecycles_table")
  instance_id = simplejson.loads(msg)['instance-id']
  logging.debug("update_cloudservice_instance_lifecycles_table: " + instance_id)
  instance_lifecycle_instance = Instance_lifecycles.objects.get(instance_id = instance_id)
  instance_lifecycle_instance.instance_launched_at = datetime.now()
  logging.debug("update_cloudservice_instance_lifecycles_table: " + str(datetime.now()))
  instance_lifecycle_instance.save()

def call(request) :
  logging.debug("!!!~~~~~!!!!~~~~~~!!!!!!~~~~~~!!!! : 1")
  if request.method == "POST":
    logging.debug("!!!~~~~~!!!!~~~~~~!!!!!!~~~~~~!!!! : 2")
    token = request.POST['token']
    channel = request.POST['userid']
    message = request.POST['vminfo']
    #ami_index = request.POST['ami_index']
    ami_index = simplejson.loads(message)['ami-launch-index']
    instance = Instances.objects.get(instance_token=token,ami_index=ami_index)
    
    if instance.launch_response_time == None  :
      logging.debug("!!!~~~~~!!!!~~~~~~!!!!!!~~~~~~!!!! : 3")
      instance.current_state = "running"
      instance.launch_response_time = datetime.now()
      instance.public_dns_name = simplejson.loads(message)['public-ipv4']
      instance.private_dns_name = simplejson.loads(message)['local-ipv4']
      instance.save()
      node_path = Configs.objects.get(key="node_path").value
      sayjs_path = Configs.objects.get(key="say.js_path").value
      if simplejson.loads(message)['event_type'] == "instance_lunched" :
        logging.debug("!!!~~~~~!!!!~~~~~~!!!!!!~~~~~~!!!! : 4")
        #sendPasswordEmail(simplejson.loads(message)['public-ipv4'],simplejson.loads(message)['linuxusername'], simplejson.loads(message)['linuxuserpassword'])
        update_cloudservice_instance_lifecycles_table(message)
        sendPasswordEmail(channel,message)
        emailNotification(channel,message)
        

        #notice_msg = "instance %s was launched with ip %s" % ( simplejson.loads(message)['instance-id'] , simplejson.loads(message)['public-ipv4'] )
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
