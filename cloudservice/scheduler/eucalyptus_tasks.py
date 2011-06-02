


# eucalyptus tasks




def getInstanceList(eucaconn) :
  return_json_str = "[]";
  try :
    reservations = euca_conn.get_all_instances()
  except Exception, ex:
    logging.error('//atmosphere/cloudservice/scheduler/eucalyptus_tasks : ' + ex)
    #euca.disaply_error_and_exit('%s' % ex)
    
    instance_ids = ""
    instance_num = 0
    instance_json_string = ""
    # reservation
    for reservation in reservations:
      reservation_string = '%s\t%s' % (reservation.id, reservation.owner_id)
      group_delim = '\t'
      for group in reservation.groups:
        reservation_string += '%s%s' % (group_delim, group.id)
        group_delim = ', '
      #print 'RESERVATION\t%s' % (reservation_string)
      instances = []
      for instance in reservation.instances:
        if instance.id in instance_ids:
          instances.append(instance)
        else:
          instances = reservation.instances
      for instance in instances:
        instance_num = instance_num + 1
        try :
          instance_name = Instances.objects.get(instance_id = instance.id).instance_name
        except :
          instance_name = ""
        try :
          instance_description = Instances.objects.get(instance_id = instance.id).instance_description
        except :
          instance_description = ""
        try :
          instance_tags = Instances.objects.get(instance_id = instance.id).instance_tags
        except :
          instance_tags = ""
        if instance:
          instance_image_name = ""
          try :
            instance_image_name = Machine_images.objects.get(image_id = instance.image_id).image_name
          except :
            instasnce_image_name = ""
          instance_json_string = instance_json_string + """
            {
              "instance_num" : "%s" ,
              "instance_name" : "%s" ,
              "instance_description" : "%s",
              "instance_tags" : "%s",
              "reservation_id" : "%s" ,
              "reservation_owner_id" : "%s" ,
              "group_id" : "%s" ,
              "instance_id" : "%s" ,
              "instance_image_id": "%s" ,
              "instance_image_name" : "%s" , 
              "instance_public_dns_name" : "%s" ,
              "instance_private_dns_name" : "%s" ,
              "instance_state" : "%s" ,
              "instance_key_name" : "%s" ,
              "instance_ami_launch_index" : "%s" ,
              "instance_product_codes" : "%s" ,
              "instance_instance_type" : "%s" ,
              "instance_launch_time" : "%s" ,
              "instance_placement" : "%s" ,
              "instance_kernel" : "%s" ,
              "instance_ramdisk" : "%s"
            }, """ % (
              instance_num ,
              instance_name ,
              instance_description.replace("\n", "<br>"),
              instance_tags , 
              reservation.id,
              reservation.owner_id ,
              group.id,
              instance.id,
              instance.image_id,
              instance_image_name,
              instance.public_dns_name,
              instance.private_dns_name,
              instance.state,
              instance.key_name,
              instance.ami_launch_index,
              instance.product_codes ,
              instance.instance_type,
              instance.launch_time,
              instance.placement,
              instance.kernel,
              instance.ramdisk
            )
      return_json_str = "[%s]" % instance_json_string[0:-2]
    a = simplejson.loads(return_json_str)
    #return simplejson.dumps(a)
    return atmo_util.jsoner("\"success\"","\"\"", simplejson.dumps(a))


def terminate_instance():
  pass

