
var machine_image_property_template = function(instance_id) {
 
 
	var r = [ '<table class="row_details">',
		'<tbody>',
		 '<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_ami_id">Name: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_machine_image_id_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_zone">ID: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_zone_value"></span></div></td></tr>',
			'<tr>',
			'<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_ami_id">Owner/Creator: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_machine_image_id_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_zone">Priviledge: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_zone_value"></span></div></td></tr>',
			'<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_security_groups">Zone:</span></span><span class="value" id="'+instance_id+'_instance_detail_panel_security_group_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_type">Status: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_type_value"></span></div></td>',
			'</tr>',
   '<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_security_groups">Kernel Image:</span></span><span class="value" id="'+instance_id+'_instance_detail_panel_security_group_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_type">Ram disk Image: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_type_value"></span></div></td>',
			'</tr>',
   '<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_security_groups">Archtecture:</span></span><span class="value" id="'+instance_id+'_instance_detail_panel_security_group_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_type">Type:</span></span><span class="value" id="'+instance_id+'_instance_detail_panel_type_value"></span></div></td>',
			'</tr>',
   '<tr>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_security_groups">Created at</span></span><span class="value" id="'+instance_id+'_instance_detail_panel_security_group_value"></span></div></td>',
				'<td style="width: 50%;"><div class="data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_type"></span></span><span class="value" id="'+instance_id+'_instance_detail_panel_type_value"></span></div></td>',
			'</tr>',
			'<tr>',
				'<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Location: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_tags_value"></span></div></td>',
			'</tr>',
   '<tr>',
				'<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Image Tags: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_tags_value"></span></div></td>',
			'</tr>',
			'<tr>',
				'<td colspan="2" style="width: 100%;"><div class="triple_wide_data"><span style="width: 180px;" class="label"><span class="console-tooltip" id="instances_main_launch_time">Image Description: </span></span><span class="value" id="'+instance_id+'_instance_detail_panel_instance_description_value"></span></div></td>',
			'</tr>',
		'</tbody></table>'];



  
  
 
  return r.join(''); 

};