#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
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
