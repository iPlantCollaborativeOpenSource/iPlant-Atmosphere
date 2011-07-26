


class Openstack_model_template():
	""" 
    this covers Openstack cloud
    openstack api: http://docs.openstack.org/cactus/openstack-compute/developer/openstack-compute-api-1.0/content/ch04s03s01.html
  """
	def __init__(self,userid,credential,endpoint):
		pass


  #category: Servers
  #action: list servers
  def list_servers(self,**kwargs):
    pass

  #category: Servers
  #action: create server
  def create_server(self,**kwargs):
    pass

  #category: Servers
  #action: get server details
  def get_server_details(self,**kwargs):
    pass

  #category: Servers
  #action: update server name / administrative password
  def update_server_name(self,**kwargs):
    pass

  def update_server_administrative_password(self,**kwargs):
    pass

  #category: Servers
  #action: delete server
  def delete_server(self,**kwargs):
    pass

  #category: Server Addresses
  #action: list addresses
  def list_addresses(self,**kwargs):
    pass

  #category: Server Addresses
  #action: list public addresses
  def list_public_addresses(self,**kwargs):
    pass

  #category: Server Addresses
  #action: list private addresses
  def list_private_addresses(self,**kwargs):
    pass

  #category: Server Addresses
  #action: share an ip address
  def share_an_ip_address(self,**kwargs):
    pass

  #category: Server Addresses
  #action: unshare an ip address
  def unshare_an_ip_address(self,**kwargs):
    pass

  #category: Server Actions
  #action: reboot server
  def reboot_server(self,**kwargs):
    pass

  #category: Server Actions
  #action: rebuild server
  def rebuild_server(self,**kwargs):
    pass

  #category: Server Actions
  #action: resize server
  def resize_server(self,**kwargs):
    pass

  #category: Server Actions
  #action: confirm resized server
  def confirm_resized_server(self,**kwargs):
    pass

  #category: Server Actions
  #action: revert resized server
  def revert_resized_server(self,**kwargs):
    pass

  #category: Flavors
  #action: list flavors
  def list_favors(self,**kwargs):
    pass

  #category: Flavors
  #action: get flavor details
  def get_flavor_details(self,**kwargs):
    pass

  #category: Images
  #action: list images
  def list_images(self,**kwargs):
    pass

  #category: Images
  #action: create image
  def create_image(self,**kwargs):
    pass

  #category: Images
  #action: get image details
  def get_image_details(self,**kwargs):
    pass

  #category: Images
  #action: delete image
  def delete_image(self,**kwargs):
    pass

  #category: Backup Schedules
  #action: list backup schedules
  def list_backup_schedules(self,**kwargs):
    pass

  #category: Backup Schedules
  #action: create/update backup schedule
  def create_update_backup_schedule(self,**kwargs):
    pass

  #category: Backup Schedules
  #action: disable backup schedule
  def diable_backup_schedule(self,**kwargs):
    pass
  
  #category: Shared IP Groups
  #action: list shared ip groups
  def list_shared_ip_groups(self,**kwargs):
    pass

  #category: Shared IP Groups
  #action: create shared IP Group
  def create_shared_ip_grou(self,**kwargs):
    pass

  #category: Shared IP Groups
  #action: get shared IP group details
  def get_shared_ip_group_detail(self,**kwargs):
    pass

  #category: Delete Shared IP Group
  #action: delete shared IP group
  def delete_shared_ip_group(self,**kwargs):
    pass