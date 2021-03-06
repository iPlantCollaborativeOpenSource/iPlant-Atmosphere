#!/usr/bin/env python
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

import logging

from atmosphere.cloudservice.models import Ec2_keys # <== not good
from atmosphere.cloudfront.models import Configs

class Login :

  def __init__(self,username,password):
    
    logging.debug(self.ec2_key_exist(username))
    
    return None

  def result():
    return False
   
  def has_a_valid_privilege_of(self, username, password):
    return False
    
  def has_a_ec2_key_of(self, username):
    ec2_keys = Ec2_keys.objects.filter(username=username)
    for e in ec2_keys:
        if username == e.username:
            return True
    return False

  def is_there_(self, username, password):
    pass

  def create_ec2_user(self,username,password):
    pass


    
  def create_ec2_user(username) :
    loggging.debug("creating ec2 user")
    
  def is_atmo_group_user(username):

    # this is due to non-secure ugly iplant ldap structure!
    #server = ldap.open("ldap.iplantcollaborative.org")  #THIS SHOULD BE FROM DATABASE!!! NOT HARDCODED!
    server = Configs.objects.get(key="ldap_server").value
    server.protocol_version = ldap.VERSION3
  
    #baseDN = "dc=iplantcollaborative,dc=org" #THIS SHOULD BE FROM DATABASE!!! NOT HARDCODED!
    baseDB = Configs.objects.get(key="ldap_server_dn").value
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    #searchFilter = "cn=atmo-user" #THIS SHOULD BE FROM DATABASE!!! NOT HARDCODED!
    searchFilter = Configs.objects.get(key="ldap_search_filter").value

    try:
      ldap_result_id = server.search(baseDN, searchScope, searchFilter, retrieveAttributes)
      result_set = []
      while 1:
        result_type, result_data = server.result(ldap_result_id, 0)
        if (result_data == []):
          break
        else:
          if result_type == ldap.RES_SEARCH_ENTRY:
            result_set = result_data[0][1]['memberUid']
    except ldap.LDAPError, e:
      logging.debug("error-> " + str(e))
  
    if username in result_set :
      create_ec2_user(username)
    else :
      logging.debug("ASDDDDDDDDDDDDDDDDDDDDDDDDDDD")
    
    
  
  def is_it_in_ec2_keys_table(username):
    ec2_keys = Ec2_keys.objects.filter(username = username)
    return True if len(ec2_keys) > 0 else False

  def ldap_auth(username,password) :
  
    server = 'ldap://ldap.iplantcollaborative.org' #THIS SHOULD BE FROM DATABASE!!! NOT HARDCODED!
    conn = ldap.initialize(server)
    dn = "uid="+username+",ou=people,dc=iplantcollaborative,dc=org" #THIS SHOULD BE FROM DATABASE!!! NOT HARDCODED!
    try :
      auth = conn.simple_bind_s(dn,password)
      if is_it_in_ec2_keys_table(username) == False :
        is_atmo_group_user(username)  
      else :
        return True
    except :
      return False
