#!/usr/bin/python

import httplib
import urllib
from urlparse import urlparse
import string
import datetime

import getpass
import json 

print """\nregisterImage version 20110310_001\n"""
username = raw_input("input your username: ")
password = getpass.getpass("input your password: ")


class MissingFieldError(Exception):
  def __init__(self,value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def getToken():
  auth_server_url = "https://atmo.iplantcollaborative.org:443/auth"
  #auth_server_url = "https://bond.iplantcollaborative.org:443/auth"
  o = urlparse(auth_server_url)
  auth_server_url = string.split(o.netloc,":")[0]
  auth_server_port = int(string.split(o.netloc,":")[1])
  auth_server_path = o.path
  method = "GET"
  params = None
  headers = {
    "Content-type" : "application/x-www-form-urlencoded",
    "Accept" : "text/plain",
    "X-Auth-User" : username,
    "X-Auth-Key" : password,
    "User-Agent" : "Atmo/CloudFront"
    }
  conn = httplib.HTTPSConnection(auth_server_url,auth_server_port)
  conn.request(method,auth_server_path,params,headers)
  r1 = conn.getresponse()
  print "HTTP RETURN CODE: %i, %s" % (r1.status,r1.reason)
  headers = r1.getheaders()
  conn.close()
  if (r1.status != 200) : exit()
  for header in headers:
    if header[0] == "x-server-management-url" :
      url = header[1]
    if header[0] == "x-auth-token" :
      token = header[1]
  return {'url':url,'token':token}

def registerImage(token):
  o = urlparse(token['url'])

  protocol = o.scheme
  url = string.split(o.netloc,":")[0]
  port = string.split(o.netloc,":")[1]
  path = o.path + "/registerImage"
  
  manifest = open('atmo_image_manifest.json','r').read()
  try :
    manifest_json = json.loads(manifest)
    if 'image_name' not in manifest_json : raise MissingFieldError('application_name does not exist')
    if 'image_id' not in manifest_json : raise MissingFieldError('machine_image does not exist')
  except Exception, e:
    print e
    print "manifest json error. please check your manifest json again"
    exit() 
  
  params = "manifest=" + urllib.quote(manifest)

  headers = {
          "Content-type" : "application/x-www-form-urlencoded",
          "Accept" : "text/plain",
          "X-Auth-User" : username,
          "X-Auth-Token" : token['token'],
          "X-Api-Server" : token['url'],
          "X-Api-Version" : "v1"
  }

  conn = httplib.HTTPSConnection(url,port)
  conn.request("POST",path,params,headers)
  r1 = conn.getresponse()
  print "HTTP RETURN CODE: %i, %s" % (r1.status,r1.reason)
  #print "HEADERS"
  #print r1.getheaders()
  #print "HEADERS END\n"
  print r1.read()

if __name__ == "__main__":
  registerImage(getToken())
