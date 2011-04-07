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

var west = {};

west.init = {
	region: 'west',
  id: 'west-panel', // see Ext.getCmp() below
  title: 'Resources Index',
  split: true,
  width: 200,
  minSize: 175,
  maxSize: 400,
  collapsible: true,
  collapsed: true,
	margins: '0 0 0 5',
  layout: { type: 'accordion', animate: true },
  items: [
		{contentEl: 'instances_tree', title: 'Cloud Instances', html: '', border: false, iconCls: 'nav', listeners: {'beforeexpand':function(){
			// I dont like this. must change it to nicer/noble codes :-)
			Ext.get('instances_tree').select('*').remove();
			var west_cloud_instances = new west.cloud_instances;
		}}},
  {contentEl: 'images_tree', title: 'Machine Images', html: '', border: false, iconCls: 'settings', listeners: {'beforeexpand':function(){ 
			Ext.get('images_tree').select('*').remove();
	 		var west_machine_images = new west.machine_images;
		}}},
  {contentEl: 'volumes_tree', title: 'Machine Volumes', html: '', border: false, iconCls: 'settings', listeners: {'beforeexpand':function(){
			Ext.get('volumes_tree').select('*').remove();
			var west_machine_volumes = new west.machine_volumes;
		}}},
  {contentEl: 'snapshots_tree', title: 'Snapshots', html: '', border: false, iconCls: 'settings', listeners: {'beforeexpand':function(){
			Ext.get('volumes_tree').select('*').remove();
			var west_machine_volumes = new west.machine_volumes;
		}}},
  {contentEl: 'keys_tree', title: 'Authentication Keys', html: '', border: false, iconCls: 'settings', listeners: {'beforeexpand':function(){ 
			// I dont like this. must change it to nicer/noble codes :-)
			Ext.get('keys_tree').select('*').remove();
			//var west_cloud_instances = new west.cloud_instances;
			ajax_common_gateway("getKeyPairsListTree","GET","", west.foo);  
		}}}
	]
};
	
west.cloud_instances = function() {
	var render = function(m) {
		var cloud_instances_json = (m == null) ? resource_request_jsonstore.getRunningInstancesTree : m ;
		this.tree = new Ext.tree.TreePanel({ 
			loader:new Ext.tree.TreeLoader(),
      width:200,
      height:400,
      rootVisible: false,
      border: false,
      //renderTo:Ext.getBody(),
      el: "instances_tree",
      id: "instanceTree",
      //renderTo: Ext.get('instances_tree'),
      root:new Ext.tree.AsyncTreeNode({
      	expanded:true,
       	leaf:false,
        text:'Tree Root',
       	children:cloud_instances_json
      }),
			listeners: {
				click: function(n) {
					center_panel_object.createTab(this.el, n.attributes.text);
				}
			}
    });
		this.tree.render();
	};
 ajax_common_gateway("getRunningInstancesTree","GET","", render);
};
	
west.machine_images = function() {
	render = function(m) {
  	//var machine_volumes_json = m;
    var machine_volumes_json = (m == null) ? resource_request_jsonstore.getMachineImageTree : m ;
    this.tree = new Ext.tree.TreePanel({
        	loader:new Ext.tree.TreeLoader(),
        	width:200,
        	height:400,
        	rootVisible: false,
        	border: false,
        	//renderTo:Ext.getBody(),
        	//el: "images_tree",
        	id: "imagesTree",
        	renderTo: Ext.get('images_tree'),
        	root:new Ext.tree.AsyncTreeNode({
          	expanded:true,
          	leaf:false,
          	text:'Tree Root',
          	children:machine_volumes_json
        	}),
				listeners: {
					click: function(n) {
						center_panel_object.createTab(this.el, n.attributes.text);
					}
				}
      	});
    	}
    	ajax_common_gateway("getMachineImageTree","GET","", render);
};
		
west.machine_volumes = function() {
	var render = function(m) {
      //var machine_volumes_json = m;
      var machine_volumes_json = (m == null) ? resource_request_jsonstore.getVolumeListTree : m ;
      this.tree = new Ext.tree.TreePanel({
        loader:new Ext.tree.TreeLoader(),
        width:200,
        height:400,
        rootVisible: false,
        border: false,
        //renderTo:Ext.getBody(),
        //el: "volumes_tree",
        id: "volumesTree",
        renderTo: Ext.get('volumes_tree'),
        root:new Ext.tree.AsyncTreeNode({
          expanded:true,
          leaf:false,
          text:'Tree Root',
          children:machine_volumes_json
        }),
        listeners: {
					click: function(n) {
						center_panel_object.createTab(this.el, n.attributes.text);
					}
				}
      });
  };
  ajax_common_gateway("getVolumeListTree","GET","", render);
};

	
		
west.authentication_keys = function() {
	var render = function(m) {
		//var authentication_keys_json = m;
		var authentication_keys_json = (m == null) ? resource_request_jsonstore.getKeyPairsListTree : m ;
		this.tree = new Ext.tree.TreePanel({
			loader:new Ext.tree.TreeLoader(),
			width:200,
   		height:300,
    	rootVisible: false,
     	border: false,
    	//renderTo:Ext.getBody(),
     	//el: "volumes_tree",
    	//id: "volumesTree",
    	renderTo: Ext.get('keys_tree'),
    	root:new Ext.tree.AsyncTreeNode({
     		expanded:true,
       	leaf:false,
       	text:'Tree Root',
       	children:authentication_keys_json
     	})
  	});
	};
	
	var foo_val = "iam125";
	var foo = function() { /*console.log("aaa");*/ };
	ajax_common_gateway("getKeyPairsListTree","GET","", render);
};

west.foo = function(m) {
	//console.log(Ext.get('keys_tree'));
	var authentication_keys_json = (m == null) ? resource_request_jsonstore.getKeyPairsListTree : m ;
	this.tree = new Ext.tree.TreePanel({
			loader:new Ext.tree.TreeLoader(),
			width:200,
   		height:300,
    	rootVisible: false,
     	border: false,
    	//renderTo:Ext.getBody(),
     	//el: "volumes_tree",
    	//id: "volumesTree",
    	renderTo: Ext.get('keys_tree'),
			root:new Ext.tree.AsyncTreeNode({
     		expanded:true,
       	leaf:false,
       	text:'Tree Root',
       	children:authentication_keys_json
     	})
  	});
	
	/*
		//var authentication_keys_json = m;
		var authentication_keys_json = (m == null) ? resource_request_jsonstore.getKeyPairsListTree : m ;
		this.tree = new Ext.tree.TreePanel({
			loader:new Ext.tree.TreeLoader(),
			width:200,
   		height:100,
    	rootVisible: false,
     	border: false,
    	//renderTo:Ext.getBody(),
     	//el: "volumes_tree",
    	//id: "volumesTree",
    	renderTo: Ext.get('keys_tree'),
    	root:new Ext.tree.AsyncTreeNode({
     		expanded:true,
       	leaf:false,
       	text:'Tree Root',
       	children:authentication_keys_json
     	})
  	});
	*/
};
	