from atmosphere.cloudservice.models import *
from tools.request_factory import RequestFactory
from cloudservice.api.v1.cloud import Ec2_cloud



rf = RequestFactory()
post_request = rf.post('/resources/v1/launchApp/', {'image_id':'emi-D9602AB9', 'instance_size':'m1.small','instance_name':'iPlant Base Image','application_id':'app1','life_time':1})

ec2_keys = Ec2_keys.objects.get(username = 'seungjin')
ec2_cloud = Ec2_cloud(ec2_access_key=str(ec2_keys.ec2_access_key),ec2_secret_key=str(ec2_keys.ec2_secret_key),ec2_url=str(ec2_keys.ec2_url),s3_url=str(ec2_keys.s3_url))

ec2_cloud.launchApp(post_request)
