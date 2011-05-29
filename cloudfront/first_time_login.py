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
    