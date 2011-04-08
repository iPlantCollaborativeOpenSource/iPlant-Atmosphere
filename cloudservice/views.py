#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
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
from atmosphere.cloudservice.library.cloud import Cloud
from atmosphere.cloudservice.models import *

# door page
def door(request) :
	# valid user goes to application
	# invalid user goes to login/gate page
	if request.user.is_authenticated():
		return HttpResponseRedirect('/application')	
	else:
		return HttpResponseRedirect('/login')
		
def logout_page(request) :
	logout(request)
	return HttpResponseRedirect('/')

def application(request) :
  logging.debug("?????")
  logging.dbug(request.user)
	if not request.user.is_authenticated() :
		return HttpResponseRedirect('/')
	template = get_template('application/application.html')
	variables = Context({
		'user' : request.user,
	})
	output = template.render(variables)
	return HttpResponse(output)

def ajax_service(request) :
	if not request.user.is_authenticated() :
		# HttpResponseForbidden
		# Acts just like HttpResponse but uses a 403 status code.
		return HttpResponseForbidden('<h1>HTTP/1.0 403 FORBIDDEN</h1>')
	method = request.META['PATH_INFO'].split('/')[2];
	logging.debug('METHOD REQUESTED: ' + method)
	#return HttpResponse(getInstanceList())
	if len(method) > 0 :
		try :
			c = Cloud(ec2_access_key=Ec2_keys.objects.get(username=request.user.username).ec2_access_key,ec2_secret_key=Ec2_keys.objects.get(username=request.user.username).ec2_secret_key)
			f=getattr(c,method)
			return HttpResponse(f(request))
		except Exception, e:
			logging.error("cloudservice.library.cloud error: %s" % e)
			print "cloudservice.library.cloud error: %s" % e
			return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT FOUND</h1>')
	else :
		logging.error("cloudservice.library.cloud error: method [%s]" % method)
		return HttpResponseNotFound('<h1>HTTP/1.0 404 METHOD NOT FOUND</h1>')

#from cloudservice.forms import *
#from django.template import RequestContext
#from django.shortcuts import render_to_response
#
#
#def register_page(request) :
#	if request.method == 'POST':
#		form = RegistrationForm(request.POST)
#		if form.is_valid() :
#			user = User.objects.create_user(
#				username=form.cleaned_data['username'],
#				password=form.cleaned_data['password1'],
#				email=form.cleaned_data['email']
#			)
#			return HttpResponseRedirect('/register/success/')
#	else:
#		form = RegistrationForm()
#	variables = RequestContext(request, { 
#		'form': form 
#	})
#	return render_to_response(
#		'registration/register.html', 
#		variables
#	)
#
#import operator
#import django.contrib.auth
#
def ec2(request) :
	if ( request.user.username == '' ) :
		return HttpResponseRedirect("/")
	template = get_template('ec2.html')
	variables = Context({
		'user' : request.user,
		'path_info' : request.META['PATH_INFO'],
	})
	output = template.render(variables)
	return HttpResponse(output)
#	
#def cloud_front(request) :
#	if ( request.user.username == '' ) :
#		return HttpResponseRedirect("/")
#	template = get_template('cloud_front.html')
#	variables = Context({
#		'user' : request.user,
#		'path_info' : request.META['PATH_INFO'],
#	})
#	output = template.render(variables)
#	return HttpResponse(output)
#
#def condor(request) :
#	if ( request.user.username == '' ) :
#		return HttpResponseRedirect("/")
#	template = get_template('condor.html')
#	variables = Context({
#		'user' : request.user,
#		'path_info' : request.META['PATH_INFO'],
#	})
#	output = template.render(variables)
#	return HttpResponse(output)
#
#def user_profile(request) :
#	if ( request.user.username == '' ) :
#		return HttpResponseRedirect("/")
#	template = get_template('user_profile.html')
#	variables = Context({
#		'user' : request.user,
#		'path_info' : request.META['PATH_INFO'],
#	})
#	output = template.render(variables)
#	return HttpResponse(output)
#
#def system_monitor(request) :
#	if ( request.user.username == '' ) :
#		return HttpResponseRedirect("/")
#	template = get_template('system_monitor.html')
#	variables = Context({
#		'user' : request.user,
#		'path_info' : request.META['PATH_INFO'],
#	})
#	output = template.render(variables)
#	return HttpResponse(output)
