#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#



class resource_template_amazon():
	pass

# July 22, 2011, @seungjin
# do I need to separate resource_template_amazon and resource_templatte_eucalyptus?
# not sure now. we will see how it ends.
# end of @seungjin

class resource_template_eucalyptus():
	pass

class resource_template_openstack():
	pass

class User(object, resource_template_amazon, resource_template_eucalyptus, resource_template_openstack) :

  def __init__(userid):
  	resource_list = []

  def load_resources():
  	pass
