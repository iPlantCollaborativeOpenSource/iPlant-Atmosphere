#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#
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
from atmosphere.cloudservice.models import *

from atmosphere.cloudservice.api.v1.cloud import *
from atmosphere.cloudauth.models import *


from boto.exception import *

import datetime

def api_request_auth(request):
  if request.META.has_key('HTTP_X_AUTH_USER') == False :
    return False
  if request.META.has_key('HTTP_X_AUTH_USER') and request.META.has_key('HTTP_X_AUTH_TOKEN') :
    user = request.META['HTTP_X_AUTH_USER']
    token = request.META['HTTP_X_AUTH_TOKEN']
    api_server = request.META['HTTP_X_API_SERVER']    
    try :
      token = Tokens.objects.get(token=token)
    except Tokens.DoesNotExist:
      return False
    d = datetime.timedelta(days=1)
    print token.api_server_url
    print api_server
    if token.user == user and token.logout == None and ( token.issuedTime + d > datetime.datetime.now() ) :
      return True
    else:
      return False
  else :
      return False
  return False

def call(request) :
  logging.debug("###############")
  # AUTH
  if api_request_auth(request) == False :
    #return HttpResponse("401 UNAUTHORIZED", status=401)
    #return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT FOUND</h1>')
    return HttpResponseForbidden('HTTP/1.0 401 UNAUTHORIZED')

  request_time = datetime.datetime.now();
  resource_method = request.META['PATH_INFO'].split('/')[3]
  http_request_method = request.META['REQUEST_METHOD']
  username = request.META['HTTP_X_AUTH_USER']
  token = request.META['HTTP_X_AUTH_TOKEN']
  api_server_url = request.META['HTTP_X_API_SERVER']
  api_version = request.META['HTTP_X_API_VERSION']
 
 
  out = None
  r = 0
  if len(resource_method) > 0 :
    try :
      ec2_keys = Ec2_keys.objects.get(username = username)
      #c = Cloud(ec2_access_key=Ec2_keys.objects.get(username=request.user.username).ec2_access_key,ec2_secret_key=Ec2_keys.objects.get(username=request.user.username).ec2_secret_key)
      c = Ec2_cloud(ec2_access_key=ec2_keys.ec2_access_key,ec2_secret_key=ec2_keys.ec2_secret_key, ec2_url=ec2_keys.ec2_url, s3_url=ec2_keys.s3_url )
      f=getattr(c,resource_method)(request)
    except NameError, e:
      logging.error("cloudservice.api.v1.resources NameError at %s: %s" % (resource_method, e))
      f = e
      r = -1
    except EC2ResponseError, e:
      logging.error("cloudservice.api.v1.resources EC2ResponseError at %s: %s" % (resource_method, e))
      f = e
      r = -1
    except Exception, e:
      logging.error("cloudservice.api.v1.resources error at %s: %s" % (resource_method, e))
      f = e
      r = 2
  else :
    #return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT DEFINED</h1>')
    r = 3
  
  # LOG API REQUEST
  requested_param = ""
  for (key,item) in request.POST.items():
    p = "%s = %s" % (key, str(item))
    requested_param = requested_param + p + "\n"
    
  if requested_param == "" :
    requested_param = None

  api_log = Api_logs(
    request_user = username,
    request_token = token,
    request_url = request.META['PATH_INFO'],
    request_remote_ip = request.META['REMOTE_ADDR'],
    request_remote_user_agent = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else None, 
    request_method = resource_method,
    http_request_method = http_request_method ,
    request_param = requested_param,
    request_time = request_time ,
    #response_value = f ,
    response_value = ''.join(str(f).splitlines()).replace('  ',''),
    response_time = datetime.datetime.now()
    )
  api_log.save()
  
  if r == 0 :
    response = HttpResponse(f)
    response['X-API-VERSION'] = "v1"
    response['Content-Type'] = "application/json; charset=utf-8"

    response['Access-Control-Allow-Origin'] = '*' 
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = '*'
    
    return response
  elif r == -1 :
    final_json = """{
    "result" : {
        "code" : "%s" ,
        "meta" : "%s" ,
        "value" : "%s"
    } 
    }""" % ("systemTrouble","internal cloud trouble", "null")
    response = HttpResponse(final_json, status=200)
    response['X-API-VERSION2'] = "2"
    return response
  elif r > 0 :
    return HttpResponse('<h1>HTTP/1.0 404 METHOD NOT DEFINED ('+str(r)+')</h1>', status=404)
