#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
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
    tokens store here
  """
  username = models.CharField(max_length=128)
  x_auth_token = models.CharField(max_length=128,null=True)
  x_cdn_management_url = models.CharField(max_length=128,null=True)
  x_server_management_url = models.CharField(max_length=128,null=True)
  date = models.CharField(max_length=128,null=True)
  x_storage_url = models.CharField(max_length=128,null=True)
  server = models.CharField(max_length=128)
  content_type = models.CharField(max_length=128,null=True)
  issued_at = models.DateTimeField(null=True)
  is_expired = models.CharField(max_length=128,null=True)

class Access_logs(models.Model):
  timestamp = models.DateTimeField(null=True)
  remote_ip = models.CharField(max_length=40,null=True)
  user_agent = models.TextField(null=True)
  url = models.CharField(max_length=256,null=True)
  http_referer = models.CharField(max_length=256,null=True)
  meta_data = models.CharField(max_length=256,null=True)
  
