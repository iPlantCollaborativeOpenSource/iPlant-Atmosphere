#!/usr/local/bin/python

import sys
import os

from euca2ools import Euca2ool, AddressValidationError, ProtocolValidationError, Util

import subprocess

# python ./port_controller.py [esteve] [22,80,443,5900,5901,5902,5903,5904,5905,5906,5907,5908,5909,5910,1247] [1247]

class PortControllerException(Exception):
  def __init__(self, value):
    self.parameter = value
  def __str__(self):
    return repr(self.parameter)


def openPort(user_list,protocol,port_list):
  #euca-authorize -p tcp -p 22 -s 0.0.0.0/0 default
  euca = None
  try:
    euca = Euca2ool('P:p:o:u:s:t:', ['protocol=', 'port-range=', 'source-group=', 'source-group-user=', 'source-subnet=', 'icmp-type-code='], compat=True)
  except Exception, e:
    print e

  for user in user_list:
    for port in port_list:
      group_name = None
      protocol = protocol
      from_port = port
      to_port = port
      source_group_name = None
      source_group_owner_id = None
      cidr_ip = None

  euca_conn = euca.make_connection()

def main():
  if len(sys.argv) != 4 :
    print "Usage: port_controller.py [user list] [TCP port list] [UDP port list]"
    print "ex) port_controller [user1,user2] [22,80,443,5900,5901,5902,5903,5904,5905,5906,5907,5908,5909,5910,1247] [1247]"
    print "ex) port_controller * [22,80,90,100] [23,24]"
    sys.exit()

  if (sys.argv[1][0] != "[" or sys.argv[1][-1] != "]") or (sys.argv[2][0] != "[" or sys.argv[2][-1] != "]") or (sys.argv[3][0] != "[" or sys.argv[3][-1] != "]"):
    print "invalid argument format"
    sys.exit()
  userList = (lambda x: map(str, x[1:-1].split(',')))(sys.argv[1])
  try:
    tcpPortList = (lambda x: map(int, x[1:-1].split(',')))(sys.argv[2])
  except ValueError:
    tcpPortList = []
  try:  
    udpPortList = (lambda x: map(int, x[1:-1].split(',')))(sys.argv[3])
  except ValueError:
    udpPortList = []

  if len(filter(lambda x: not os.path.exists(os.getcwd()+"/odin-"+x+"-x509/eucarc"),userList)) > 0 :
    print "User %s does/do not exit" % str(filter(lambda x: not os.path.exists(os.getcwd()+"/odin-"+x+"-x509/eucarc"),userList)) 
    sys.exit()


  run_cmd = lambda c : subprocess.Popen(c.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False).stdout.read()
  
  for user in userList:
    print user
    euca = None
    my_EC2_ACCESS_KEY = None
    my_EC2_SECRET_KEY = None
    my_EC2_URL = None
    my_S3_URL = None
    eucarc_file = None
    eucarc_file = open(os.getcwd()+"/odin-"+user+"-x509/eucarc",'r')
    for line in eucarc_file.readlines():
      if line[0] != "#" and line.split()[0] == "export":
        #setattr(self,line.split()[1].split("=",1)[0],line.split()[1].split("=",1)[1])
        #globals()[ "my_"+line.split()[1].split("=",1)[0] = line.split()[1].split("=",1)[1]]
        #locals()[ "my_%s" % line.split()[1].split("=",1)[0] ] = line.split()[1].split("=",1)[1]   
        #exec 'my_%s = %s' % (line.split()[1].split("=",1)[0], line.split()[1].split("=",1)[1])
        #setattr(euca,line.split()[1].split("=",1)[0],line.split()[1].split("=",1)[1])
        if line.split()[1].split("=",1)[0] == "EC2_ACCESS_KEY" :
          my_EC2_ACCESS_KEY = line.split()[1].split("=",1)[1][1:-1]
        if line.split()[1].split("=",1)[0] == "EC2_SECRET_KEY" :
          my_EC2_SECRET_KEY = line.split()[1].split("=",1)[1][1:-1]
        if line.split()[1].split("=",1)[0] == "EC2_URL" :
          my_EC2_URL = line.split()[1].split("=",1)[1]
        if line.split()[1].split("=",1)[0] == "S3_URL" :
          my_S3_URL = line.split()[1].split("=",1)[1] 
        
    try:
      euca = Euca2ool('P:p:o:u:s:t:', ['protocol=', 'port-range=', 'source-group=', 'source-group-user=', 'source-subnet=', 'icmp-type-code='], compat=True)
      #euca = Euca2ool()
      euca.ec2_user_access_key = my_EC2_ACCESS_KEY
      euca.ec2_user_secret_key = my_EC2_SECRET_KEY
      euca.ec2_url = my_EC2_URL
      euca.s3_url = my_S3_URL

      euca_conn = euca.make_connection()
    except Exception, e:
      print "\neuca conn error\n" + str(e)
    
    for tcp_port in tcpPortList:
      group_name = "default"
      protocol = "tcp"
      from_port = tcp_port
      to_port = tcp_port
      source_group_name = None
      source_group_owner_id = None
      cidr_ip = "0.0.0.0/0"

      euca.validate_address(cidr_ip)
      euca.validate_protocol(protocol)
      
      #euca_conn = euca.make_connection()
      try:
        return_code = euca_conn.authorize_security_group(group_name = group_name,
          src_security_group_name = source_group_name,
          src_security_group_owner_id = source_group_owner_id,
          ip_protocol = protocol,
          from_port = tcp_port,
          to_port = tcp_port,
          cidr_ip = cidr_ip)
        print "\t%s %s %s" % (str(return_code), protocol, from_port)
      except Exception, ex:
        print "\tauth cmd error\n" + str(ex)

    for udp_port in udpPortList:
      group_name = "default"
      protocol = "udp"
      from_port = udp_port
      to_port = udp_port
      source_group_name = []
      source_group_owner_id = []
      cidr_ip = "0.0.0.0/0"  
      #euca_conn = euca.make_connection()

      try:
        return_code = euca_conn.authorize_security_group(group_name = group_name,src_security_group_name = source_group_name,src_security_group_owner_id = source_group_owner_id,ip_protocol = protocol,from_port = from_port,to_port = to_port,cidr_ip = cidr_ip)
        print "\t%s %s %s" % (str(return_code), protocol, from_port)
      except Exception, ex:
        print ex

if __name__ == "__main__":
  main()



#python ./port_controller.py [esteve] [22,80,443,5900,5901,5902,5903,5904,5905,5906,5907,5908,5909,5910,1247] [1247]
