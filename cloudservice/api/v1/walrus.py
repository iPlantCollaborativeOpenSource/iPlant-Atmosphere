#!/usr/bin/env python

#
# Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
# This software is licensed under the CC-GNU GPL version 2.0 or later.
# License: http://creativecommons.org/licenses/GPL/2.0/
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

import getopt, sys, os
import logging


my_euca_storage = "http://150.135.78.127:8773/services/Walrus"
my_euca_access = "4iNIDXPptlD20Ywnh8Gu9fKdrJLhoDUSX8ibHg"
my_euca_secret = "QiYbTUsoLmMQKCnKHUFBIQ27U7dOl3kbI0SDaA"

my_euca_host = "150.135.78.127"
my_euca_port = 8773
my_euca_path = "/services/Walrus"

#iplant_aws_access = 'AKIAIS4KCWHHCMC3AIGQ'
#iplant_aws_secret = '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'

from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat


conn = S3Connection(my_euca_access,
                    my_euca_secret,
                    is_secure=False,
                    host=my_euca_host,
                    port=my_euca_port,
                    path=my_euca_path,
                    #provider='eucalyptus',
                    #bucket_class=Bucket,
                    calling_format=OrdinaryCallingFormat(),
                    debug=0)



bucket = conn.create_bucket('test')
from boto.s3.key import Key
k = Key(bucket)
k.key = 'foobar'
k.set_contents_from_string('hello world')

rs = conn.get_all_buckets()
for b in rs:
  print b



#mehods


def create_bucket():
  pass

def get_all_buckets():
  pass

def set_contents():
  pass


