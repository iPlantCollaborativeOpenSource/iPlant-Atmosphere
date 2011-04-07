/**
 *
 * Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
 * This software is licensed under the CC-GNU GPL version 2.0 or later.
 * License: http://creativecommons.org/licenses/GPL/2.0/
 *
 * Author: Seung-jin Kim
 * Contact: seungjin@email.arizona.edu 
 * Twitter: @seungjin
 * 
 **/

var instance_property_template = function(instance_id) {				
	var r = '<table class="row_details">\
		<tbody>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_name">Inatance Name: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_name_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instance_detail_panel_instances_id">Instance ID: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_id_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_ami_id">Machine Image ID: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_machine_image_id_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_zone">Zone: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_zone_value"></span></div></td></tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_security_groups">Security Groups: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_security_group_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_type">Type: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_type_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_status">Status: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_status_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_owner">Owner: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_owner_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_virtualization">Virtualization: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_virtualization_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_reservation">Reservation: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_reservation_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_platform">Platform: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_platform_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_key_pair_name">Key Pair Name: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_key_pair_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_kernel_id">Kernel ID: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_kernel_id_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_ram_disk_id">RAM Disk ID: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_ramdisk_id_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_public_dns">Public DNS: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_public_dns_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_private_dns">Private DNS: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_private_dns_value"></span></div></td>\
			</tr>\
			<tr>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Launch Time: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_launch_time_value"></span></div></td>\
				<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_lifecycle">Lifecycle: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_lifecycle_value"></span></div></td>\
			</tr>\
			<tr>\
				<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="block_device">Block Device: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_block_device_value"></span></div></td>\
			</tr>\
			<tr>\
				<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Instance Tags: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_tags_value"></span></div></td>\
			</tr>\
			<tr>\
				<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Instance Description: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_description_value"></span></div></td>\
			</tr>\
		</tbody></table>';
	return r;
};