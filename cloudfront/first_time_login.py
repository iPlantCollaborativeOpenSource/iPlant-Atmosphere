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
import commands

class First_time_login:
    
  def __init__(self,username,password):
    self.make_new_ec2_acct()
    return None

  def make_new_ec2_acct(sekf):
    # java -classpath "./jars/*:./com:." Rufus username, name, email, newpassword
    a = commands.getstatusoutput('java -classpath "./tools/rufus/jars/*:./tools/rufus/com:./tools/rufus/." Rufus test test test test')
    logging.debug(a)
    pass

  def update_ec2_key_table():
    pass
    
