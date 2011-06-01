#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

-- 
-- 2/7/2011
alter table cloudservice_api_logs add request_remote_user_agent varchar(128)

-- 2/9/2011
alter table cloudservice_applications ADD machine_image_user_data_scripts_script_id varchar(128);
alter table cloudservice_machine_images ADD machine_image_user_data_scripts_script_id varchar(128);

-- 3/10/2011
alter table cloudservice_machine_images ADD COLUMN registered_at timestamptz

-- 3/16/2011
ALTER TABLE "public"."cloudservice_instance_launch_hooks" ALTER COLUMN "webhook_header_params" TYPE text;
ALTER TABLE "public"."cloudservice_instance_launch_hooks" ALTER COLUMN "responsed_header" TYPE text;

------



