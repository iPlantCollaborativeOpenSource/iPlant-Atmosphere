#
# Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
# This software is licensed under the CC-GNU GPL version 2.0 or later.
# License: http://creativecommons.org/licenses/GPL/2.0/
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

from django.http import HttpResponse
from atmosphere.cloudauth.models import *

import uuid
import logging
import datetime
from datetime import timedelta

import sys
import ldap

def ldap_validate(username,password):
    server_obj = Configs.objects.filter(key='ldap_server').order_by('value')[0]
    server = server_obj.value
    conn = ldap.initialize(server)
    ldap_server_dn_obj = Configs.objects.filter(key='ldap_server_dn').order_by('value')[0]
    ldap_server_dn_value = ldap_server_dn_obj.value    
    dn = "uid="+username+","+ldap_server_dn_value
    try :
        auth = conn.simple_bind_s(dn,password)
        return True
    except :
        return False


def auth(request):
    if request.META.has_key('HTTP_X_AUTH_KEY') and request.META.has_key('HTTP_X_AUTH_USER') :
        x_auth_user = request.META['HTTP_X_AUTH_USER']
        x_auth_key = request.META['HTTP_X_AUTH_KEY']
        if ldap_validate(x_auth_user,x_auth_key) == True:
            return auth_response(request)
        else :
            return HttpResponse("401 UNAUTHORIZED", status=401)
    else :
        return HttpResponse("401 UNAUTHORIZED", status=401)

def auth_response(request):
  
  api_server_url = Configs.objects.filter(key='api_server_url').order_by('value')[0]
  
  #login validation
  #return HttpResponse("hello",mimetype="text/plain" )
  response = HttpResponse()
  #response.write("heelo it is me")
  response['X-Server-Management-Url'] = api_server_url.value
  response['X-Storage-Url'] = "http://"
  response['X-CDN-Management-Url'] = "http://"
  token = str(uuid.uuid4())
  response['X-Auth-Token'] = token
  #print request
  auth_user_token = Tokens(user=request.META['HTTP_X_AUTH_USER'],token=token,issuedTime=datetime.datetime.now(),remote_ip=request.META['REMOTE_ADDR'],api_server_url=api_server_url.value)
  auth_user_token.save()
  return response


def validate_token(request):
    if request.META.has_key('HTTP_X_AUTH_USER') and request.META.has_key('HTTP_X_AUTH_TOKEN') :
        user = request.META['HTTP_X_AUTH_USER']
        token = request.META['HTTP_X_AUTH_TOKEN']
        api_server = request.META['HTTP_X_AUTH_API_SERVER']
        
        try :
            token = Tokens.objects.get(token=token)
        except Tokens.DoesNotExist:
            return HttpResponse("401 UNAUTHORIZED", status=401)
        
        d = timedelta(days=1)
        
        if token.user == user and token.logout == None and ( token.issuedTime + d > datetime.datetime.now() ) and token.api_server_url == api_server :
            return HttpResponse("Valid token")
        else:
            return HttpResponse("401 UNAUTHORIZED", status=401)
    else :
        return HttpResponse("401 UNAUTHORIZED", status=401)