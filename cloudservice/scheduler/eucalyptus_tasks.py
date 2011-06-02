#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


# Djago ORM use


from celery.task import task
from datetime import datetime

import boto
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo



def write_log(msg):
  file = open("/home/atmosphere_dev/atmosphere/logs/scheduler.log","a")
  a = datetime.now()
  stmt = a.strftime("%A, %d. %B %Y %I:%M%p %S") + " >>> " + msg
  file.write(stmt+"\n") 

@task
def hello_world():
  write_log("hello_world")

@task
def getInstanceList() :
  region = RegionInfo(name="eucalyptus", endpoint="...")
  connection = boto.connect_ec2(aws_access_key_id='...',
                              aws_secret_access_key='...',
                              is_secure=False,
                              region=region,
                              port=8773,
                              path="/services/Eucalyptus")
  images = connection.get_all_images()
  write_log(str(images))

@task
def terminate_instance(eucaconn):
  pass



getInstanceList()