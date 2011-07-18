#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#


from django.conf.urls.defaults import *



import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


site_media = os.path.join(os.path.dirname(__file__), 'site_media')
mobile = os.path.join(os.path.dirname(__file__), 'mobile')
admin_media = os.path.join(site_media,'admin')

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Example:
    # (r'^atmosphere/', include('atmosphere.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Systemwide
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),


    # My application settings
    #(r'^$', 'cloudservice.views.door') ,
    #(r'^login/$', 'django.contrib.auth.views.login') ,
    #(r'^logout/$', 'cloudservice.views.logout_page') ,
    #(r'^application/$', 'cloudservice.views.application') ,
    #(r'^register/$', register_page),
    #(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
    #(r'^ec2/$', 'cloudservice.views.ec2'),
    #(r'^cloud_front/$', cloud_front),
    #(r'^condor/$', condor),
    #(r'^user_profile/$', user_profile),
    #(r'^system_monitor/$', system_monitor),

    # AJAX Communication protocol
    # this wil be a legacy protocol
    #(r'^ajax_service/', 'cloudservice.views.ajax_service') ,
    
    # AUTH
    (r'^auth$', 'atmosphere.cloudauth.auth.auth') ,
    (r'^auth/validate_token$','atmosphere.cloudauth.auth.validate_token'),
    
    # resources call
    (r'^resources/v1/', 'atmosphere.cloudservice.api.v1.resources.call') , 
    (r'^resources/v2/', 'atmosphere.cloudservice.api.v2.resources.call') ,

    # instance service
    (r'^instanceservice/','atmosphere.cloudservice.api.v1.instanceservice.call'),

    # vis test
    #(r'^vis/one', 'atmosphere.cloudfront.vis.one') ,

    # default
    (r'^$', 'atmosphere.cloudfront.views.door'),
    #(r'^pv1/login/$', 'django.contrib.auth.views.login' , {'template_name': 'application_pv1/login.html'}) ,
    (r'^login/$', 'atmosphere.cloudfront.views.login'),
    (r'^logout/$', 'atmosphere.cloudfront.views.logout_page') ,
    (r'^application/$', 'atmosphere.cloudfront.views.application') ,
    
    
    ##################
    (r'^resource_request/(?P<method>.*)$', 'atmosphere.cloudfront.views.resource_request'),
    ##################
    
    (r'^first_time_login/$', 'atmosphere.cloudfront.views.first_time_login'),

    ###################
    (r'^mobile/(?P<path>.*)$', 'django.views.static.serve', {'document_root': mobile}),

    (r'^admin_media/(.*)', 'django.views.static.serve', {'document_root' : admin_media, 'show_indexes' : True}),

)

