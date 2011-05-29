#!/usr/bin/env python

#!/usr/bin/env python

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



def call(request) :
  return HttpResponse('api version 2 : not scheduled')