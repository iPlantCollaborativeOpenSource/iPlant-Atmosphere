/**
 * The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
 *
 * Project: Atmosphere, iPlant Collaborative
 * Author: Seung-jin Kim
 * Twitter: @seungjin
 * GitHub: seungjin
 *
 **/

require([
    "/site_media/scripts/center/instance_panel.js",
    "/site_media/scripts/center/application_information_panel.js",
    "/site_media/scripts/center/machine_image_panel.js",
    "/site_media/scripts/center/machine_volume_panel.js"
], function() { });

var center = function(){

  var application_stack = JSON.parse(sessionStorage.getItem('__getAppList')).result.value
  
  
  var app_stack_html = [];
  for (k=0;  k < application_stack.length; k++ ) {
    if ( ( application_stack[k].application_icon_path == null ) || ( application_stack[k].application_icon_path == "None" ) ) {
      var b = '<div id="app_icon"><input type="image" app_name="'+application_stack[k].application_name+'" src="/site_media/images/app_icons/icons/default.png" name="'+application_stack[k].application_name+'" onclick="application_icon_clicked(this);" onmouseover="application_icon_mouseover(this);" onmouseout="application_icon_mouseout(this)" "/>' + application_stack[k].application_name + '</div>';
    } else {
      var b = '<div id="app_icon"><input type="image" app_name="'+application_stack[k].application_name+'" src="' + application_stack[k].application_icon_path + '" name="'+application_stack[k].application_name+'" onclick="application_icon_clicked(this);" onmouseover="application_icon_mouseover(this);" onmouseout="application_icon_mouseout(this)" "/>' + application_stack[k].application_name + '</div>';
    }
    app_stack_html.push(b);
  }  
  app_stack_html = app_stack_html.join('')
    
  center_panel_object = this;

  this.application_info_tooltip = function(t,application_name) {
    //document.getElementById("ss").src = "/site_media/images/app_icons/MILK_XL_11/Icons/ECG_color.png";
    //console.log(application_name);
    
    new Ext.ToolTip({
      target: t,
      anchor: 'top',
      showDelay: 0,
      hideDelay: 0,
      anchorOffset: 20, // center the anchor on the tooltip
      html: "<style type=\"text/css\"> fixed250 { width: 250px; display: block; }</style> <fixed250><b>App: "+application_name+"</b><hr/>"+this.a+"</fixed250>"
    });
    
  };
  
  this.application_icon_mouseover = function(o) {
    o.src = (function(){ t=o.src.split("."); t[o.src.split(".").length-2] = t[o.src.split(".").length-2]+"_"; return(t.join(".")); }());
    for (k=0;  k < application_stack.length; k++ ) {
      if ( application_stack[k].application_name === o.name) {
        desc = "<p class='app_name'>"+ application_stack[k].application_name+ "</p>" + application_stack[k].application_description;
        Ext.DomHelper.overwrite("app_desc",desc);
      };
    };
    document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/click1.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
  };
  
  
  this.application_icon_clicked = function(o) {
		var a = JSON.parse(sessionStorage.getItem("__getAppList"));
		var s = a.result.value.length
		for ( i = 0; i< s; i++ ) {
    	if ( o.name === a.result.value[i].application_name) {
				app_machine_id = a.result.value[i].machine_image_id;
				machine_size = a.result.value[i].system_minimum_requirements;
    application_id = a.result.value[i].application_id;
			};
		}
		if (app_machine_id === 'None') {
			document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/doh.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
			Ext.MessageBox.alert('Msg','Service is not available yet.');
		} else {
		  param = "image_id=" + app_machine_id + "&" + "instance_size=" + machine_size + "&" + "instance_name=" + o.name + "&application_id=" + application_id;
		  var lanchingAppMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Launching "+o.name+". Please wait..."});
		  lanchingAppMsg.show();
			
		  ajax_common_gateway("launchApp", "POST", param,
      success_callback_function = function(){
        lanchingAppMsg.hide();
        document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/excellent.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
        Ext.MessageBox.alert('Message', "Successfully initiated your app. <br/>Please wait 10 to 15 min to finish the request. <br/>Your App id is <b><font color='#408080'>" + JSON.parse(sessionStorage.getItem("__launchApp")).result.value + "</font></b>");
      },
      fail_callback_function = function() {
        lanchingAppMsg.hide();
        document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/doh.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
        a = JSON.parse(sessionStorage.getItem("__launchApp")).result.value;
        Ext.MessageBox.alert('Message', "<b><font color='#408080'>Your quota is over.</font></b><br/>Current resource use: "+a.current_cpu+" cpu, "+a.current_mem+"M mem<br/>Quota : "+a.limit_cpu+" cpu, "+a.limit_mem+"M mem");
      }
    );
		}
  };
  
  this.application_icon_mouseout = function(o) {
    o.src = function(){ t=o.src.split("."); t[t.length-2] = t[t.length-2].substr(0,t[t.length-2].length-1); return t.join("."); }();
    Ext.DomHelper.overwrite("app_desc","");
  }
	
  this.application_info = function(application_name) {
    Ext.DomHelper.overwrite('application_name',application_name);
  };
  
  
 
 
  var aa = function() {
    //console.log(Ext.query('#applications').height);
    
    
    //console.log("222");
    return 200
  };
  

  var applications = new Ext.Panel({
    id : 'applications',
    title: 'App Desktop',
    bodyCfg : {  },
    items: [
      { region: 'north',
        bodyCfg : { style: { 'margin' : '10px' } },
        border: false,
        split: true,
        height: aa(),
        html : app_stack_html,
        autoScroll:true
      },
      {//title: 'South Region is resizable',
        region: 'south', // position for region,
        split: true, // enable resizing
        bodyCfg : { style: { 'margin' : '10px' } },
        html: application_information_template(),
        layout: 'fit',
        frame: false,
        border: false,
        autoScroll:true
      }
    ]
  });

  var app_catalog = new Ext.Panel({
    id : 'app_catalog',
    title: 'App Catalog',
    bodyCfg : {  },
    items: [
      { region: 'north',
        bodyCfg : { style: { 'margin' : '10px' } },
        border: false,
        split: true,
        height: aa(),
        html : "App catalog here. User can add their own app into their app desktop",
        autoScroll:true
      },
      {//title: 'South Region is resizable',
        region: 'south', // position for region,
        split: true, // enable resizing
        bodyCfg : { style: { 'margin' : '10px' } },
        html: application_information_template(),
        layout: 'fit',
        frame: false,
        border: false,
        autoScroll:true
      }
    ]
  });
  



/*

  console.log(application_stack);
  
  
   var tpl = new Ext.XTemplate(
		'<tpl for=".">',
            '<div class="thumb-wrap" id="{name}">',
		    '<div class="thumb"><img src="{url}" title="{name}"></div>',
		    '<span class="x-editable">{shortName}</span></div>',
        '</tpl>',
        '<div class="x-clear"></div>'
	);




    var applications = new Ext.Panel({
    id : 'applications',
    title: 'Applications',
    bodyCfg : {  },
    items: 
      new Ext.DataView({
        region: north,
            store: application_stack,
            tpl: tpl,
            autoHeight:true,
            emptyText: 'No images to display',

            plugins: [
                new Ext.DataView.DragSelector(),
                new Ext.DataView.LabelEditor({dataIndex: 'application_name'})
            ],

            prepareData: function(data){
                data.shortName = Ext.util.Format.ellipsis(data.name, 15);
                data.sizeString = Ext.util.Format.fileSize(data.size);
                data.dateString = data.lastmod.format("m/d/Y g:i a");
                return data;
            },
            
            listeners: {
            	selectionchange: {
            		fn: function(dv,nodes){
            			var l = nodes.length;
            			var s = l != 1 ? 's' : '';
            			panel.setTitle('Simple DataView ('+l+' item'+s+' selected)');
            		}
            	}
            }
        })

  });

  
*/
  

  var dashboard_accordion = new Ext.Panel({
    id: 'dashboard',
    title: 'Advanced',
    layout: 'accordion',
    defaults: {
      // applied to each contained panel
      bodyStyle: 'padding:10px',
      bodyCfg: { cls: 'x-panel-body dashboard' },
      collapsed: true
    },
    listeners: {},
    bodyCfg: { cls: 'x-panel-body dashboard_background' },
    layoutConfig: { // layout-specific configs go here
      titleCollapse: true,
      animate: true
    },
    items: [{
      title: 'Launch new instance',
      contentEl: 'launch_new_instance',
      listeners: { 'beforeexpand': function(){ } },
      autoScroll: true
    },{
      title: 'Running instances index',
      contentEl: 'running_instances_index',
      listeners: {
        'beforeexpand': function(){
          //instance_grid.running_instances_index_store.load();
          //activation_register("running_instances_index"); 
          ajax_common_gateway("getInstanceList", "GET", "", function(){ instance_grid.update(); });
        }
      }
    },{
      title: 'Machine images management',
      contentEl: 'machine_images_management',
      listeners: {
        'beforeexpand': function(){
        //machine_image_grid.image_index_store.load();
        ajax_common_gateway("getImageList", "GET", "", machine_image_grid.update);
        }
      },
    autoScroll: true
    },{
	  title: 'Volume storage management',
	  contentEl: 'volume_storage_management',
	  listeners: {
		'beforeexpand': function(){
		  ajax_common_gateway("getVolumeList", "GET", "", volume_storage_grid.update);
		}
	  },
	  autoScroll: true
	},{
	  title: 'Snapshots management',
	  contentEl: 'snapshots_management',
	  listeners: {
		'beforeexpand': function(){
		//ajax_common_gateway("getKeyPairsList", "GET", "", keys_grid.update);
	  }
	},
	autoScroll: true
  },{
	  title: 'Authentication keys management',
	  contentEl: 'authentication_keys_management',
	  listeners: {
		'beforeexpand': function(){
		  ajax_common_gateway("getKeyPairsList", "GET", "", keys_grid.update);
		}
	  },
	  autoScroll: true
	}]
  });




  var machine_images = new Ext.Panel({
    id : 'machine_images',
    title: 'Machine Images',
    bodyCfg : {  },
    items: [
      { region: 'north',
        bodyCfg : { style: { 'margin' : '10px' } },
        border: false,
        split: true,
        height: aa(),
        html : "s",
        autoScroll:true
      },
      {//title: 'South Region is resizable',
        region: 'south', // position for region,
        split: true, // enable resizing
        bodyCfg : { style: { 'margin' : '10px' } },
        html: application_information_template(),
        layout: 'fit',
        frame: false,
        border: false,
        autoScroll:true
      }
    ]
  });

  var volumes = new Ext.Panel({
    id : 'volumes',
    title: 'Volumes',
    bodyCfg : {  },
    items: [
      { region: 'north',
        bodyCfg : { style: { 'margin' : '10px' } },
        border: false,
        split: true,
        height: aa(),
        html : "s",
        autoScroll:true
      },
      {//title: 'South Region is resizable',
        region: 'south', // position for region,
        split: true, // enable resizing
        bodyCfg : { style: { 'margin' : '10px' } },
        html: application_information_template(),
        layout: 'fit',
        frame: false,
        border: false,
        autoScroll:true
      }
    ]
  });
  
  var snapshots = new Ext.Panel({
    id : 'snapshots',
    title: 'Snapshots',
    bodyCfg : {  },
    items: [
      { region: 'north',
        bodyCfg : { style: { 'margin' : '10px' } },
        border: false,
        split: true,
        height: aa(),
        html : "s",
        autoScroll:true
      },
      {//title: 'South Region is resizable',
        region: 'south', // position for region,
        split: true, // enable resizing
        bodyCfg : { style: { 'margin' : '10px' } },
        html: application_information_template(),
        layout: 'fit',
        frame: false,
        border: false,
        autoScroll:true
      }
    ]
  });

  this.centralTabs = new Ext.TabPanel({
    region: 'center', // a center region is ALWAYS required for border layout
    resizeTabs: true,
    minTabWidth: 115,
    enableTabScroll: true,
    deferredRender: false,
    activeTab: 0, // first tab initially active
    //defaults: {autoScroll:true},
    //plugins: new Ext.ux.TabCloseMenu(),
    listeners: {
      //render: function(tabPanel){ dashboard(); }
    },
    //items: [applications, dashboard_accordion, machine_images, volumes, snapshots]
    items: [applications, app_catalog, dashboard_accordion]
  });

  this.dashboard = function(){};
  


  var getInstanceInfoHandler = function(m) {
	//volume_index_store.loadData((m == null) ? resource_request_jsonstore.getVolumeList : m);
	//
	//console.log(resource_request_jsonstore.getInstanceInfo);
	group_id = resource_request_jsonstore.getInstanceInfo[0][0].group_id;
	instance_ami_launch_index = resource_request_jsonstore.getInstanceInfo[0][0].instance_ami_launch_index;
	instance_description = resource_request_jsonstore.getInstanceInfo[0][0].instance_description;
	instance_id = resource_request_jsonstore.getInstanceInfo[0][0].instance_id;
	instance_image_id = resource_request_jsonstore.getInstanceInfo[0][0].instance_image_id
	instance_image_name = resource_request_jsonstore.getInstanceInfo[0][0].instance_image_name;
	instance_instance_type = resource_request_jsonstore.getInstanceInfo[0][0].instance_instance_type
	instance_kernel = resource_request_jsonstore.getInstanceInfo[0][0].instance_kernel;
	instance_key_name = resource_request_jsonstore.getInstanceInfo[0][0].instance_key_name;
	instance_launch_time = resource_request_jsonstore.getInstanceInfo[0][0].instance_launch_time;
	instance_name = resource_request_jsonstore.getInstanceInfo[0][0].instance_name;
	instance_num = resource_request_jsonstore.getInstanceInfo[0][0].instance_num;
	instance_placement = resource_request_jsonstore.getInstanceInfo[0][0].instance_placement;
	instance_private_dns_name = resource_request_jsonstore.getInstanceInfo[0][0].instance_private_dns_name;
	instance_product_codes = resource_request_jsonstore.getInstanceInfo[0][0].instance_product_codes;
	instance_public_dns_name = resource_request_jsonstore.getInstanceInfo[0][0].instance_public_dns_name;
	instance_ramdisk = resource_request_jsonstore.getInstanceInfo[0][0].instance_ramdisk;
	instance_state = resource_request_jsonstore.getInstanceInfo[0][0].instance_state;
	instance_tags = resource_request_jsonstore.getInstanceInfo[0][0].instance_tags;
	reservation_id = resource_request_jsonstore.getInstanceInfo[0][0].reservation_id;
	resservation_owner_id = resource_request_jsonstore.getInstanceInfo[0][0].reservation_owner_id;

	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_instance_name_value",instance_name);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_instance_id_value",instance_id);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_machine_image_id_value",instance_image_id);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_zone_value",instance_placement);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_security_group_value","default");
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_type_value",instance_instance_type);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_status_value",instance_state);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_owner_value",resservation_owner_id);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_virtualization_value","Paravirtual, Euca-Xen");
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_reservation_value",reservation_id);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_platform_value",'-');
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_key_pair_value",instance_key_name);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_kernel_id_value",instance_kernel);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_ramdisk_id_value",instance_ramdisk);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_public_dns_value",instance_public_dns_name);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_private_dns_value",instance_private_dns_name);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_launch_time_value",instance_launch_time);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_lifecycle_value","normal");
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_instance_tags_value",instance_tags);
	Ext.DomHelper.overwrite(instance+"_instance_detail_panel_instance_description_value",instance_description);
  };


  var getInstanceInfo = function(instance_panel_name){
	var instance_info = ""
	instance = instance_panel_name.substring(instance_panel_name.indexOf('(') + 1, instance_panel_name.indexOf(')'))
	param = "instance_id=" + instance;
	ajax_common_gateway("getInstanceInfo","POST",param, getInstanceInfoHandler);
  };


  var getVolumeInfo = function() {
	param = "";
	ajax_common_gateway("getVolumeList","POST",param, getVolumeInfoHandler);
  }


  var attacheClicked = function() {
	// instance_id = req.POST['instance_id']
	//device = req.POST['device']
	//volume_id = req.POST['volume_id']
	i_id = centralTabs.activeTab.id.split("(")[1].split(")")[0];
	param = "instance_id=" + i_id + "&device=sdb&volume_id="+this.text;
	ajax_common_gateway("attachVolume","POST",param, attacheClickedHandler);
  };

  var attacheClickedHandler = function() {
	instance_panel_name = centralTabs.activeTab.id.substring(6);
	Ext.MessageBox.show({
	  title: 'Please wait',
	  msg: 'Processing request...',
	  progressText: 'Initializing...',
	  width:300,
	  progress:true,
	  closable:false,
	  animEl: 'mb6'
	});
	// this hideous block creates the bogus progress
    var f = function(v){
      return function(){
        if(v == 12){
          Ext.MessageBox.hide();
          //Ext.example.msg('Done', 'Your fake items were loaded!');
		  getVolumeInfo();
        }else{
          var i = v/11;
          Ext.MessageBox.updateProgress(i, Math.round(100*i)+'% completed');
        }
      };
    };

	for(var i = 1; i < 13; i++){
	  setTimeout(f(i), i*500);
	};

	getVolumeInfo();
  };

  var detacheClicked = function() {
	if (this.text != "No volume available") {
	  //console.log(this.text);	
	  //console.log(this.instance);
	  param = "instance_id=" + this.instance_id + "&device=sdb&volume_id="+this.text;
	  ajax_common_gateway("detachVolume","POST",param,detacheClickedHandler);
	}
  };

  var detacheClickedHandler = function() {
    instance_panel_name = centralTabs.activeTab.id.substring(6);
    Ext.MessageBox.show({
      title: 'Please wait',
      msg: 'Processing request...',
      progressText: 'Initializing...',
      width:300,
      progress:true,
      closable:false,
      animEl: 'mb6'
    });
	// this hideous block creates the bogus progress
    var f = function(v){
      return function() {
        if(v == 12){
          Ext.MessageBox.hide();
          //Ext.example.msg('Done', 'Your fake items were loaded!');
		  getVolumeInfo();
        } else {
          var i = v/11;
          Ext.MessageBox.updateProgress(i, Math.round(100*i)+'% completed');
        }
      };
    };

    for(var i = 1; i < 13; i++){
      setTimeout(f(i), i*500);
    };

    getVolumeInfo();
  };

  var getVolumeInfoHandler = function() {
    available_volume_list = [];
    inuse_volume_list = [];
 
    //for (var i = 0; i < resource_request_jsonstore.getVolumeList.length; i++) {
    for (var i = 0; i < JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value.length; i++) {
	  if (JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].status == "available") {
		//console.log(resource_request_jsonstore.getVolumeList[i]);
		//o = "No block device";
		Ext.DomHelper.overwrite(instance+"_instance_detail_panel_block_device_value","");
		
		available_volume_list.push({
		  text: JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].id,
		  iconCls: "_icon",
		  handler: attacheClicked
		})
		
	  } else if (JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].status == "in-use") {
		//console.log(resource_request_jsonstore.getVolumeList[i]);
		attach_data_instance_id = JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].attach_data_instance_id;
		instance = centralTabs.activeTab.id.split("(")[1].split(")")[0];
		if (Ext.get(attach_data_instance_id + "_instance_detail_panel_block_device_value") != null) {
		  o = "/dev/" + JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].attach_data_device + "=" + JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].id + " : Size(G) " + resource_request_jsonstore.getVolumeList[i].size + " : Attached Time -" + resource_request_jsonstore.getVolumeList[i].attach_data_attach_time;
		  Ext.DomHelper.overwrite(attach_data_instance_id + "_instance_detail_panel_block_device_value", o);
		}
		
		inuse_volume_list.push({
		  text: JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].id,
		  iconCls: "_icon",
		  handler: detacheClicked,
		  instance: JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value[i].attach_data_instance_id
		});
		
	  }
	}
  };

  var serviceNotAvailable = function() {
	Ext.MessageBox.alert('Msg','Service is not available yet.' );
  };

  var terminateInstanceButtonHandler = function() {
	terminate_instance(this.instance_panel_name)
  };

  var availableVolumeList = [{text:"No volume available", iconCls:"_icon"}];
  var inuseVolumeList = [{text:"No volume available", iconCls:"_icon"}];

  var instance_info_panel_refresh = function(instance_panel_name) { 
    console.log("refresh: "+instance_panel_name);
	ajax_common_gateway("getVolumeList","POST",param, function(){ instance_info_panel(instance_panel_name); getVolumeInfoHandler();});
	instance_info_panel(instance_panel_name);
  }

  var instance_info_panel = function(instance_panel_name) {
	getVolumeInfo();
    //availableVolumeList = [{"text":"vol-7EFB0793","iconCls":"_icon"},{"text":"vol-7E560788","iconCls":"_icon"}];
    //availableVolumeList = JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value;
	// need to clean up and polish below... :-)
	a = JSON.parse(sessionStorage.getItem("__getVolumeList")).result.value;
    b = [];
	c = [];
    for ( i = 0 ; i < a.length; i++ ) {
	  if ( a[i].status === "available" ) {
		b.push({ "text" : a[i].id, "iconCls":"_icon", "handler": attacheClicked });
	  } else { c.push({ "text" : a[i].id, "iconCls":"_icon", "handler": detacheClicked }); }
	  
	}
    availableVolumeList = b;
	inuseVolumeList = c;
	getInstanceInfo(instance_panel_name);
	//instance_id = instance_panel_name.substring(instance_panel_name.indexOf('(') + 1, instance_panel_name.indexOf(')'))
        instance_id = instance_panel_name.split("(")[name.split("(").length-1].split(")")[0]
	var tb = new Ext.Toolbar();
	tb.add({
      text: 'Terminate',
	  iconCls: '_icon',
	  tooltip: 'Terminate this instance',
	  instance_id: "a",
	  instance_panel_name: instance_panel_name,
	  handler: terminateInstanceButtonHandler
    });
	tb.add({xtype:'tbseparator'});
	tb.add({
	  text: 'Refresh',
	  iconCls: '_icon',
	  tooltip: 'Refresh',
	  instance_id: "a",
	  instance_panel_name: instance_panel_name,
	  //handler: function() { Ext.MessageBox.alert('Message','I am working on - msg from seungjin'); }
	  handler: function() { instance_info_panel_refresh(instance_panel_name); }
	});
	tb.add({xtype:'tbseparator'});
	tb.add({
	  text: 'Edit',
	  iconCls: '_icon',
	  tooltip: 'Edit',
	  instance_id: "a",
	  instance_panel_name: instance_panel_name,
	  handler: function() { Ext.MessageBox.alert('Message','I am working on - msg from seungjin'); }
	});
	tb.add({xtype:'tbseparator'});
	// add a Button with the menu
	tb.add({
	  text:'Attach Volume',
	  iconCls: '_icon', instance_panel_name: instance_panel_name,
      //menu: attacheVolumeMenu  // assign menu by instance,
      instance_id: instance_id,
	  menu: availableVolumeList				
    });
	tb.doLayout();
	tb.add({xtype:'tbseparator'});
	tb.add({
	  text: 'Detach Volume',
	  iconCls: '_icon',
	  instance_panel_name: instance_panel_name,
	  //handler: function() { Ext.MessageBox.alert('Message','I am working on'); }
      menu: inuseVolumeList
    });
	tb.add({xtype:'tbseparator'});
	tb.add({
      text: 'Advanced',
	  iconCls: '_icon',
	  tooltip: 'Advanced',
	  instance_id: "a",
	  instance_panel_name: instance_panel_name,
	  handler: function() { Ext.MessageBox.alert('Message','Currently not available')}
	});
	var r = new Ext.Panel({
	  id: instance_id,
	  title: "<img src='/site_media/ext-3.2.0/resources/images/access/menu/checked.gif'/> EC2 Instance: " + instance_panel_name,
	  layout: 'border',
	  height: 600,
	  bodyBorder: false,
	  tbar: tb,
	  items: [{
	  	//title: 'Center Region',
		region: 'center', // center region is required, no width/height specified
		margins: '0 0 0 0',
		minSize: 440,
		layout: 'fit',
		frame: false,
		border: false,
		autoScroll:true,
		html: instance_property_template(instance_id)
		},{
		//title: 'South Region is resizable',
		region: 'south', // position for region,
		split: true, // enable resizing
		height: 160,
		minSize: 100,
		margins: '0 0 0 0',
		html: "",
		layout: 'fit',
		frame: false,
		border: false,
		autoScroll:true
		}
	  ]
	});
	return r;
  }				
  var emi_info_panel = function(emi_panel_name) {
 
    emi_id = emi_panel_name.substring(emi_panel_name.indexOf('(') + 1, emi_panel_name.indexOf(')'))
    
    var r = new Ext.Panel({
	  			id: emi_id,
	  			title: "<img src='/site_media/ext-3.2.0/resources/images/access/menu/checked.gif'/> Atmosphere Machine Image: " + emi_panel_name,
	  			layout: 'border',
	  			height: 600,
					bodyBorder: false,

	  			items: [{
	  				//title: 'Center Region',
						region: 'center', // center region is required, no width/height specified
						margins: '0 0 0 0',
						minSize: 440,
						layout: 'fit',
						frame: false,
						border: false,
						autoScroll:true,
						html: machine_image_property_template(emi_id)
					},{
						//title: 'South Region is resizable',
						region: 'south', // position for region,
						split: true, // enable resizing
						height: 160,
						minSize: 100,
						margins: '0 0 0 0',
						html: "",
						layout: 'fit',
						frame: false,
						border: false,
						autoScroll:true
					}]
					});
					return r;
   }

  var volume_info_panel = function(emi_panel_name) {
 
    emi_id = emi_panel_name.substring(emi_panel_name.indexOf('(') + 1, emi_panel_name.indexOf(')'))
    
    var r = new Ext.Panel({
	  			id: emi_id,
	  			title: "<img src='/site_media/ext-3.2.0/resources/images/access/menu/checked.gif'/> Atmosphere Volumes: " + emi_panel_name,
	  			layout: 'border',
	  			height: 600,
					bodyBorder: false,

	  			items: [{
	  				//title: 'Center Region',
						region: 'center', // center region is required, no width/height specified
						margins: '0 0 0 0',
						minSize: 440,
						layout: 'fit',
						frame: false,
						border: false,
						autoScroll:true,
						html: "snapshot button here"
					},{
						//title: 'South Region is resizable',
						region: 'south', // position for region,
						split: true, // enable resizing
						height: 160,
						minSize: 100,
						margins: '0 0 0 0',
						html: "",
						layout: 'fit',
						frame: false,
						border: false,
						autoScroll:true
					}]
					});
					return r;
   }

			this.createTab = function(type, resource_name){
				
				var instance_tab_add = function(){
					
					centralTabs.add({
						id: "panel_" + resource_name,
						title: "&#187;" + resource_name,
						//iconCls: 'tabs',
						bodyStyle: 'padding:0px',
						//html: testMU + ' <div id="instance_detail"><form><input type="button" value="Terminate this instance" name="button2" onClick="terminate_instance(\''+instance_id+'\')"><\/form><\/div>',
						//html: intance_panel_html(instance_id),
						items:  instance_info_panel(resource_name),
						closable: true
					}).show();
					
				}
				
				var image_tab_add = function(){
					centralTabs.add({
						id: "panel_" + resource_name,
						title: "&#187;" + resource_name,
						//iconCls: 'tabs',
						//html: ' <div id="instance_detail"><form><input type="button" value="Terminate this instance" name="button2" onClick="terminate_instance(\''+instance_id+'\')"><\/form><\/div>',
						layout: 'anchor',
						defaults: {
							// applied to each contained panel
							bodyStyle: 'padding:6px',
							bodyCfg: {}
						},
						closable: true,
						items: emi_info_panel(resource_name)
					}).show();
				}
				
				var volume_tab_add = function(){
					centralTabs.add({
						id: "panel_" + resource_name,
						title: "&#187;" + resource_name,
						//iconCls: 'tabs',
						//html: ' <div id="instance_detail"><form><input type="button" value="Terminate this instance" name="button2" onClick="terminate_instance(\''+instance_id+'\')"><\/form><\/div>',
						layout: 'anchor',
						defaults: {
							// applied to each contained panel
							bodyStyle: 'padding:6px',
							bodyCfg: {}
						},
						closable: true,
						items: volume_info_panel(resource_name)
					}).show();
				}
				
				var key_tab_add = function(){
					centralTabs.add({
						id: "panel_" + resource_name,
						title: "&#187;" + resource_name,
						//iconCls: 'tabs',
						//html: ' <div id="instance_detail"><form><input type="button" value="Terminate this instance" name="button2" onClick="terminate_instance(\''+instance_id+'\')"><\/form><\/div>',
						layout: 'anchor',
						defaults: {
							// applied to each contained panel
							bodyStyle: 'padding:6px',
							bodyCfg: {}
						},
						closable: true,
						items: []
					}).show();
				};
				switch (type.id) {
					case "instances_tree":
						instance_tab_add();
						break;
					case "imagesTree":
						image_tab_add();
						break;
					case "volumesTree":
      volume_tab_add();
						break;
					case "keys_tree":
						break;
					default:
					//
				}
			};
			
			this.terminate_instance = function(instance_panel_name){
				instance_id = instance_panel_name.substring(instance_panel_name.indexOf('(')+1,instance_panel_name.indexOf(')'));
				var terminatingVmMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Terminating your VM. Please wait..."});
				terminatingVmMsg.show();
				param = "instance_id=" + instance_id;
				ajax_common_gateway("terminateInstance", "POST", param, function(){
					//should refresh/update west panel 
					//console.log(instance_grid);
					terminatingVmMsg.hide();
	        this.centralTabs.remove("panel_"+instance_panel_name);
				} );
				//ajax_common_gateway("getInstanceList", "GET", "", instance_grid.update);
				
				/*
				
				instance_id = instance_panel_name.substring(instance_panel_name.indexOf('(') + 1, instance_panel_name.indexOf(')'))
				var conn = new Ext.data.Connection();
				conn.request({
					url: '/resource_request/terminateInstance',
					method: 'POST',
					params: {
						"instance_id": instance_id
					},
					success: function(responseObject){
						//west_cloud_instances.tree_category_root.reload();
						instance_grid.running_instances_index_store.load();
						this.centralTabs.remove("panel_" + instance_panel_name);
					},
					failure: function(){
						//Ext.Msg.alert('Status', 'Unable to show history at this time. Please try again later.');
					}
				});
				//tree.root.reload();
				//var west = new West;
				//var west_cloud_instances = new west.cloud_instances;
				//parent.cloud_instance_tree.root.reload();
				*/
			}
			
			return this.centralTabs;
			
		};
