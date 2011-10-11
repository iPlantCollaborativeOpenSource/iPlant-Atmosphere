#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

import sys
import ldap
import logging
import httplib
import urllib
import urllib2
import datetime

# django http libraries
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# django template library
from django.template import Context
from django.template.loader import get_template

# django utils
from django.utils import simplejson

# atmosphere libraries
from atmosphere.cloudservice.models import Ec2_keys
from atmosphere.cloudfront.models import *
from atmosphere.cloudfront.login import Login
from atmosphere.cloudfront.user import User as WUser
from atmosphere.cloudfront.first_time_login import First_time_login
from atmosphere.cloudfront.resource import request as r_request
from atmosphere.cloudfront.resource import getToken as getToken

def access_log(request,meta_data=None):
  access_log = Access_logs(
    timestamp = datetime.datetime.now(),
    remote_ip = request.META['REMOTE_ADDR'],
    user_agent = request.META['HTTP_USER_AGENT'],
    url = request.META['PATH_INFO'],
    http_referer = request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else None,
    meta_data = meta_data
  )
  access_log.save()

def door(request) :
  access_log(request) 
  return HttpResponseRedirect('/application') if request.session.get('authorized') else HttpResponseRedirect('/login')
 
def login(request):
  access_log(request)
  username = request.POST['username'] if 'username' in request.POST else None 
  password = request.POST['password'] if 'password' in request.POST else None
  template = get_template('application/login.html')
  variables = Context({})
  output = template.render(variables)
  if (username is None ) or (password is None):
    return HttpResponse(output) 
  user = WUser(username,password)
  #if (user.is_authorized_ldap_user == True) and (user.is_in_atmo_ldap_group == True) and (user.has_ec2_key == False) :
  #  #return HttpResponseRedirect('/first_time_login')
  #  return first_time_login(request)
  ##return HttpResponseRedirect('/application') if user.is_authorized else HttpResponse(output) # return login_failed else login_succeed               
  #if user.is_authorized :
  #  #get Token
  #  return HttpResponseRedirect('/application') if getToken(request,username,password) else HttpResponse(output)
  #else:
  #  return HttpResponse(output)
  return HttpResponseRedirect('/application') if getToken(request,username,password) else HttpResponse(output)

def logout_page(request) :
  return HttpResponseRedirect('/')

def application(request) :
  try :
    access_log(request,meta_data = "{'userid' : '%s', 'token' : '%s', 'api_server' : '%s'}" %(request.session['username'],request.session['token'],request.session['api_server']))
    template = get_template('application/application.html')
  except:
    return HttpResponseRedirect('/login')  


  #logging.debug(request);
  #REMOTE_ADDR
  #SERVER_ADDR
  #logging.debug(request.META)
  #logging.debug(request.session['api_server'])
  
  #variables = Context({
  #    'userid' : request.session['username'],
  #    'token' : request.session['token'],
  #    'api_server' : request.session['api_server']
  #})
  variables = Context({})
  output = template.render(variables)
  return HttpResponse(output)

def resource_request(request,method) :
  a = r_request(request,method)
  return HttpResponse(a)
  

def first_time_login(request):
  """
  username = request.POST['username'] if 'username' in request.POST else None
  password = request.POST['password'] if 'password' in request.POST else None
  
  ftl = First_time_login(username,password)
  logging.debug(ftl)
  
  template = get_template('application/first_time_login.html')
  variables = Context({})
  output = template.render(variables)
  return HttpResponse(output)
  """
  #return HttpResponseRedirect(reverse('/login/', kwargs={"a":"b","c":"d"}))
  return HttpResponseRedirect('/login/')
  
#def ajax_service(request) :
#  if not request.user.is_authenticated() :
#    # HttpResponseForbidden
#    # Acts just like HttpResponse but uses a 403 status code.
#    return HttpResponseForbidden('<h1>HTTP/1.0 403 FORBIDDEN</h1>')
#  method = request.META['PATH_INFO'].split('/')[3];
#  print method
#  logging.debug('METHOD REQUESTED: ' + method)
#  #return HttpResponse(getInstanceList())
#  if len(method) > 0 :
#    try :
#      c = Cloud(ec2_access_key=Ec2_keys.objects.get(username=request.user.username).ec2_access_key,ec2_secret_key=Ec2_keys.objects.get(username=request.user.username).ec2_secret_key)
#      f=getattr(c,method)
#      return HttpResponse(f(request))
#    except Exception, e:
#      logging.error("?cloudfront.library.cloud error: %s" % e)
#      print "cloudfront.library.cloud error: %s" % e
#      return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT FOUND</h1>')
#  else :
#    logging.error("cloudservice.library.cloud error: method [%s]" % method)
#    return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT FOUND</h1>')
  
