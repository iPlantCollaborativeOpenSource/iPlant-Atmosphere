#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

from datetime import datetime
from datetime import timedelta


import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from boto.utils import get_instance_metadata


from atmosphere.cloudservice.models import *
from urlparse import urlparse
from django.utils import simplejson
import atmosphere.cloudservice.api.v1.util as atmo_util

import inspect

def get_all_volume_list():
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
  volumes = connection.get_all_volumes(owner="edwintest")
  
  for volume in volumes:
    print "--\n%s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n\n" % (volume.attach, volume.attach_data, volume.attachment_state, volume.connection, volume.create_snapshot, volume.create_time, volume.delete, volume.detach, volume.endElement, volume.id, volume.item, volume.region, volume.size, volume.snapshot_id, volume.snapshots, volume.startElement, volume.status, volume.update, volume.volume_state, volume.zone)
    
  #tasks = Tasks(task_name=inspect.stack()[0][3],task_result=''.join(return_json_str.splitlines()).replace('  ',''))
  #tasks.save()