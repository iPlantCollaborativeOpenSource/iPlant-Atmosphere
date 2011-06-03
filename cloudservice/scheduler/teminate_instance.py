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

def terminate_instance(instance_id = None):
  ec2_key = Configs.objects.get(key = "admin_ec2_access_key").value
  ec2_secret = Configs.objects.get(key = "admin_ec2_secret_key").value
  ec2_url = Configs.objects.get(key = "admin_ec2_url").value
  region = RegionInfo(name="eucalyptus", endpoint=urlparse(ec2_url).netloc.split(":")[0])
  connection = boto.connect_ec2(aws_access_key_id=str(ec2_key),
  								              aws_secret_access_key=str(ec2_secret),
                              	is_secure=False,
                              	region=region,
                              	port=8773,
                              	path="/services/Eucalyptus")
  terminated_instance_list = connection.terminate_instances(instance_ids = [instance_id])

  # log it / update database