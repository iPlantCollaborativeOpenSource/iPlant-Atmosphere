#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


def jsoner(code,meta,value):
  final_json = """{"result":{"code":%s, "meta":%s, "value":%s}}""" % (code,meta,value)
  return final_json
