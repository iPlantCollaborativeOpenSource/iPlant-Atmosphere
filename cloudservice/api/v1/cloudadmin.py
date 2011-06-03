#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
# This software is licensed under the CC-GNU GPL version 2.0 or later.
# License: http://creativecommons.org/licenses/GPL/2.0/
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

import logging, sys, os
from euca2ools import Euca2ool, InstanceValidationError, SizeValidationError, SnapshotValidationError, VolumeValidationError, Util
from atmosphere.cloudservice.models import *

from django.db.models import Avg, Min, Max
import time


class CloudAdmin(object):
  
  def __init__(self):
    self.access_key = Configs.objects.get(key="admin_ec2_access_key").value
    self.secret_key = Configs.objects.get(key="admin_ec2_secret_key").value
    self.ec2_url = Configs.objects.get(key="admin_ec2_url").value
    
  def getInstanceTypeSize(self):
    #to use atmosphere for amazonaws
    #os.environ['EC2_URL'] = 'https://' + region + ".ec2.amazonaws.com"
    euca = Euca2ool('', ['region='])
    euca.ec2_user_access_key = str(self.access_key)
    euca.ec2_user_secret_key = str(self.secret_key)
    euca.ec2_url = str(self.ec2_url)
    zone_ids = "verbose"
    euca_conn = euca.make_connection()
    zones = euca_conn.get_all_zones(zone_ids)
    typeSize = []
    zonename = zones[0].name
    for zone in zones[2:]:
      typeSize.append((zonename,zone.name[3:],zone.state.split()[3],zone.state.split()[4],zone.state.split()[5]))
      #zone_string = '%s\t%s' % (zone.name, zone.state)
      #if region:
      #  zone_string += '\t%s' % region
      #  print 'AVAILABILITYZONE\t%s' % (zone_string)
    return typeSize
  
  def avgInstanceLaunchTime(self):
  
    instances = Instances.objects.all()
    return instances
    #select avg(launch_response_time - launch_request_time)  from cloudservice_instances
    #from django.db import connection, transaction
    #cursor = connection.cursor()
    # Data modifying operation - commit required
    #cursor.execute("select min(launch_response_time-launch_request_time) as min, max(launch_response_time-launch_request_time) as max, avg(launch_response_time-launch_request_time) as avg from cloudservice_instances")
    #transaction.commit_unless_managed()
    # Data retrieval operation - no commit required
    #cursor.execute("select avg(launch_response_time - launch_request_time)  from cloudservice_instances")
    #row = cursor.fetchone()
    #min_launch_time = row[0]
    #max_launch_time = row[1]
    #avg_launch_time = row[2]
    #min_seconds = min_launch_time.seconds
    #max_seconds = max_launch_time.seconds
    #avg_seconds = avg_launch_time.seconds
    #print time.strftime("%H:%M:%S",time.gmtime(min_seconds))
    #print max_seconds
    #print avg_seconds
    #return row

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  