#
# Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
# This software is licensed under the CC-GNU GPL version 2.0 or later.
# License: http://creativecommons.org/licenses/GPL/2.0/
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

from django.db import models

class Configs(models.Model):
  """ 
    system configuration / key-value pair
  """
  key = models.TextField()
  value = models.TextField()

class Tokens(models.Model):
    """
        tokens
    """
    user = models.CharField(max_length=128)
    token = models.TextField(unique=True)
    issuedTime = models.DateTimeField()
    remote_ip = models.CharField(max_length=128,null=True)
    user_agent = models.TextField(null=True)
    api_server_url = models.CharField(max_length=256)
    logout = models.CharField(max_length=128,null=True)