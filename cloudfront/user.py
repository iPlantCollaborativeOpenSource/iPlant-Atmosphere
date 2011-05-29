#!/usr/bin/env python
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#
#

import logging
import ldap

from atmosphere.cloudservice.models import Ec2_keys

class User:
  
  is_authorized = False 
  is_authorized_ldap_user = False
  is_in_atmo_ldap_group = False
  has_ec2_key = False
  
  ldap_server = "ldap://ldap.iplantcollaborative.org"
  
  def __init__(self,username,password):
    self.is_authorized_ldap_user = self.set_is_aurhorized_ldap_user(username,password)
    self.is_in_atmo_ldap_group = self.set_is_in_atmo_ldap_group(username)
    self.has_ec2_key = self.set_has_ec2_key(username)
    self.is_authorized = True if self.is_authorized_ldap_user and self.is_in_atmo_ldap_group and self.has_ec2_key else False
    return None
  
  def set_is_aurhorized_ldap_user(self,username,password):
    ldap_connection = ldap.initialize(self.ldap_server)
    dn = "uid=" + username + ",ou=People,dc=iplantcollaborative,dc=org"
    try :
      auth = ldap_connection.bind_s(dn,password)
      ldap_connection.unbind()
      return True
    except ldap.LDAPError, e:
      ldap_connection.unbind()
      return False
  
  def set_is_in_atmo_ldap_group(self,username):
    ldap_connection = ldap.initialize(self.ldap_server)
    ldap_connection.protocol_version = ldap.VERSION3
    baseDN = "dc=iplantcollaborative,dc=org"
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    searchFilter = "cn=atmo-user"
    try :
      ldap_result_id = ldap_connection.search(baseDN, searchScope, searchFilter, retrieveAttributes)
      result_type,result_data = ldap_connection.result(ldap_result_id,0)
      if result_type == ldap.RES_SEARCH_ENTRY :
        try :
          a = result_data[0][1]['memberUid'].index(username)
          return True
        except :
          return False
        return True if ( username in result_data[0][1]['memberUid']) else False
    except ldap.LDAPError, e:
      return False
  
  def set_has_ec2_key(self,username):
    return True if len(Ec2_keys.objects.filter(username=username)) > 0 else False
    
