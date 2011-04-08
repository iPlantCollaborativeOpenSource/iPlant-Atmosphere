#!/usr/bin/env python
#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#


def jsoner(code,meta,value):
  final_json = """{
    "result" : {
        "code" : %s ,
        "meta" : %s ,
        "value" : %s
    } 
  }""" % (code,meta,value)
  return final_json
