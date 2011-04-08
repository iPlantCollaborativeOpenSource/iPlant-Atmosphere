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

from atmosphere.cloudservice.models import *



import token_validation
    
    

def server(request) :
    
    if token_validation.validate_access(request) == True :

        #getServer
        
        #postServer

        return HttpResponse("hello")


    else :
        return HttpResponse("401 UNAUTHORIZED", status=401)
        

def postServer(request):
    pass
    
def getServer(request):
    
    
