#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from celery.decorators import task
from celery.task.schedules import crontab 
from celery.decorators import periodic_task  

from urlparse import urlparse
from django.utils import simplejson

from datetime import datetime
from datetime import timedelta

import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

from atmosphere.cloudservice.models import *
import atmosphere.cloudservice.api.v1.util as atmo_util


# this function launches atmosphere worker vm in atmosphere and passing its task/job to workers