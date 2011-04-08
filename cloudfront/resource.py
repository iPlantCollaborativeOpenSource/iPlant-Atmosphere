#!/usr/bin/env python
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

import logging
import httplib
import urllib
from urlparse import urlparse
import string
import datetime

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

from atmosphere.cloudfront.models import *


def getToken(request, username, password):

  auth_server_url_obj = Configs.objects.filter(key="auth_server_url").order_by('value')[0]
  auth_server_url = auth_server_url_obj.value
  o = urlparse(auth_server_url)
  auth_server_url = string.split(o.netloc,":")[0]
  auth_server_port = int(string.split(o.netloc,":")[1])
  auth_server_path = o.path
  method = "GET"
  params = None  
  headers = {
    "Content-type" : "application/x-www-form-urlencoded",
    "Accept" : "text/plain",
    "X-Auth-User" : username,
    "X-Auth-Key" : password,
    "User-Agent" : "Atmo/CloudFront" 
  }
  conn = httplib.HTTPSConnection(auth_server_url,auth_server_port)
  conn.request(method,auth_server_path,params,headers)
  r1 = conn.getresponse()
  headers = r1.getheaders()
  conn.close()
  api_service_url = None
  api_service_token = None
  for header in headers:
    if header[0] == "x-server-management-url" :
      api_service_url = header[1]
    if header[0] == "x-auth-token" :
      api_service_token = header[1]
  issued_token = Tokens(username = username, x_auth_token = api_service_token, x_server_management_url = api_service_url, issued_at = datetime.datetime.now())
  issued_token.save()
  request.session['username'] = username
  request.session['token'] = api_service_token
  request.session['api_server'] = api_service_url
  return True
  
def request(request,method):
  # emulating
  # ./resource_request seungjin e1463572-517a-41c7-a43c-5a3eb884562e GET http://bond.iplantcollaborative.org:8000/resources/v1/getImageList

  if request.session.has_key('username') == False:
    return HttpResponseForbidden('HTTP/1.0 401 UNAUTHORIZED')
  username = request.session['username']
  token = request.session['token']
  method_type = str(request.META['REQUEST_METHOD'])
  resource_url = request.session['api_server'] + "/" + method
  o = urlparse(resource_url)
  protocol = o.scheme
  url = string.split(o.netloc,":")[0]
  port = int(string.split(o.netloc,":")[1])
  path = o.path + "/"
  params = None

  if str(method_type).upper() == "GET" :
    params = '&'.join( [ u"%s=%s"%(f,v) for f,v in request.GET.iteritems() if f])
  elif str(method_type).upper() == "POST":
    params = '&'.join( [ u"%s=%s"%(f,v) for f,v in request.POST.iteritems() if f])
    
  headers = {
    "Content-type" : "application/x-www-form-urlencoded",
    "Accept" : "text/plain",
    "X-Auth-User" : username,
    "X-Auth-Token" : token,
    "X-Api-Server" : request.session['api_server'] + "/",
    "X-Api-Version" : "v1",
    "User-Agent" : "Atmo/CloudFront"
  }
  
  logging.debug(params)
  conn = httplib.HTTPSConnection(url,port)
  conn.request("POST",path,params,headers)
  r1 = conn.getresponse()
  return r1.read()
