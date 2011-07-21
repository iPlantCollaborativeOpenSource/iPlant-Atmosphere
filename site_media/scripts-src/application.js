/**
 * The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
 *
 * Project: Atmosphere, iPlant Collaborative
 * Author: Seung-jin Kim
 * Twitter: @seungjin
 * GitHub: seungjin
 *
 **/


// appllication.js
// this is a main file.


Ext.BLANK_IMAGE_URL = "/site_media/images/1x1t.gif";
sessionStorage.clear(); // init previous sessionStorage

//initial import

// It works but I need to reorganize this!

require(["/site_media/scripts/utils/ajax_common_gateway.js"], function() {

  ajax_common_gateway("getUserProfile", "GET", "", function(){ 
    for ( var i in JSON.parse(sessionStorage.getItem('__getUserProfile')).result.value ) {
      a =JSON.parse(sessionStorage.getItem('__getUserProfile')).result.value[i];
      for (var j in a) {
        if(a.hasOwnProperty(j)) sessionStorage.setItem(j,a[j]);
      }
    };
    
    ajax_common_gateway("getAppList", "GET", "", function(){ 

      require([
        "/site_media/scripts/north.js",
        "/site_media/scripts/south.js",
        "/site_media/scripts/east.js",
        "/site_media/scripts/west.js",
        "/site_media/scripts/center.js",
        "/site_media/scripts/euca_actions.js",
        "/site_media/scripts/utils/sessionStorageDebugger.js"
    		], function() { init(); });
      });     
    });

});


// global variables <- dont
/*
var center_panel_object = {};
var cloud_instance_tree = {};
var machine_image_grid = {};
var instance_grid = {};
var volume_storage_grid  = {};
var keys_grid = {};
var west_cloud_instances = {};

*/

// let's use sessionStorage
//




var resource_request_jsonstore = {};


// current working module store
var active_module_array = new Array();
var Active_module = function() { }
Active_module.prototype.add = function(m) {
  for ( var i = 0; i < active_module_array.length; i++) { if ( m === active_module_array[i] ) { var m = null; } };
  if ( m !== null ) { active_module_array.push(m); }
  //console.log(active_module_array);
}
Active_module.prototype.remove = function(m) {
  
}
Active_module.prototype.search = function(m) {
  
}
var active_module = new Active_module();
// end of current working module store


// Instances grid
var Instance_grid = function() {
  
  var running_instances_index_store = new Ext.data.JsonStore({
    fields: ['instance_name' ,'instance_description' ,'instance_tags' ,
      'reservation_id','reservation_owner_id','group_id','instance_id','instance_image_id',
      'instance_image_name','instance_public_dns_name','instance_private_dns_name',
      'instance_state','instance_key_name','instance_ami_launch_index','instance_product_codes',
      'instance_instance_type','instance_launch_time','instance_placement','instance_kernel','instance_ramdisk'],
    root: ""
  })
  
  this.init = function(m) {
    running_instances_index_store.loadData({});
    new Ext.grid.GridPanel({
      renderTo: 'running_instances_index',
      frame: false,
      //title: 'Instances' ,
      autoHeight: true ,
      viewConfig: {forceFit: true} ,
      border: false,
      store: running_instances_index_store ,
      columns: [
        {header: "Name", dataIndex: 'instance_name', width: 130, sortable: true},
        {header: "Description", dataIndex: 'instance_description', width: 300, sortable: true},
        {header: "Tags", dataIndex: 'instance_tags', width: 100, sortable: true, hidden: true},
        {header: "Researvation", dataIndex: 'reservation_id', width: 100, sortable: true, hidden: true},
        {header: "Owner id", dataIndex: 'reservation_owner_id', width: 100, sortable: true, hidden: true},
        {header: "Group id", dataIndex: 'group_id', width: 100, sortable: true, hidden: true, hidden: true},
        {header: "Instance id", dataIndex: 'instance_id', width: 100, sortable: true},
        {header: "Machine Image Name", dataIndex: 'instance_image_name', width: 100, sortable: true},
        {header: "Machine Image", dataIndex: 'instance_image_id', width: 100, sortable: true},
        {header: "Public dns name", dataIndex: 'instance_public_dns_name', width: 100, sortable: true},
        {header: "Private dns name", dataIndex: 'instance_private_dns_name', width: 100, sortable: true, hidden: true},
        {header: "Key name", dataIndex: 'instance_key_name', width: 100, sortable: true},
        {header: "State", dataIndex: 'instance_state', width: 100, sortable: true},
        {header: "Ami index", dataIndex: 'instance_ami_launch_index', width: 100, sortable: true, hidden: true},
        {header: "P.Codes", dataIndex: 'instance_product_code', width: 100, sortable: true, hidden: true},
        {header: "Machine size", dataIndex: 'instance_instance_type', width: 100, sortable: true},
        {header: "Launch Time", dataIndex: 'instance_launch_time', width: 100, sortable: true},
        {header: "Placement", dataIndex: 'instance_placement', width: 100, sortable: true, hidden: true},
        {header: "Kernel", dataIndex: 'instance_kernel', width: 100, sortable: true, hidden: true},
        {header: "Ramdisk", dataIndex: 'instance_ramdisk', width: 100, sortable: true, hidden: true}
      ]
    });
  }
  
  this.update = function(m) {
    //running_instances_index_store.loadData(m);
    active_module.add("center.dashboard.instance_grid");
    running_instances_index_store.loadData((m == null) ? resource_request_jsonstore.getInstanceList : m);
  }

}


// machine grid
var Machine_image_grid = function() {
  
  var machine_index_store = new Ext.data.JsonStore({
    fields: ['image_name','image_description','image_tags','image_id' ,'image_location','image_ownerid','image_state','image_is_public',
             'image_product_codes','image_architecture','image_type','image_ramdisk_id','image_kernel_id'],
    root: ""
  });
  
  this.init = function(m) {
    machine_index_store.loadData({});
    new Ext.grid.GridPanel({
      renderTo: 'machine_images_management',
      frame: false,
      //title: 'Machine images' ,
      autoHeight: true ,
      viewConfig: {forceFit: true} ,
      border: false,
      store: machine_index_store,
      columns: [
        { header: "Name", dataIndex: 'image_name', width: 180, sortable: true},
        { header: "Description", dataIndex: 'image_description', width: 350, sortable: true},
        { header: "Image id", dataIndex: 'image_id', width: 150, sortable: true},
        { header: "Location", dataIndex: 'image_location', width: 300, sortable: true, hidden: true} ,
        { header: "Owner id", dataIndex: 'image_ownerid', width: 100, sortable: true } ,
        { header: "Privilege", dataIndex: 'image_is_public', width: 70, sortable: true },
        { header: "State", dataIndex: 'image_state', width: 100, sortable: true },
        { header: "Code" , dataIndex: 'image_product_codes', width: 100, sortable: true, hidden: true },
        { header: "Arch" , dataIndex: 'image_architecture', width: 100, sortable: true, hidden: true  },
        { header: "Type" , dataIndex: 'image_type', width: 100, sortable: true, hidden: true  },
        { header: "Ramdisk" , dataIndex: 'image_ramdisk_id', width: 100, sortable: true, hidden: true  },
        { header: "Kernel" , dataIndex: 'image_kernel_id', width: 100, sortable: true, hidden: true  },
        { header: "Tags", dataIndex: 'image_tags', width: 120, sortable: true}
      ]
    });
  };
  
  this.update = function(m) {
    //machine_index_store.loadData(m);
    active_module.add("center.dashboard.machine_image_grid");
    machine_index_store.loadData((m == null) ? resource_request_jsonstore.getImageList : m);
  }

}


// volume storage managaement
var Volume_storage_grid = function() {
  
  var volume_index_store = new Ext.data.JsonStore({
    fields: [ 'no', 'name', 'description', 'tags', 'id', 'size', 'snapshot_id', 'status',
      'create_time', 'attach_data_instance_id', 'attach_data_device', 'attach_data_attach_time' ],
    root: ""
  });
  
  this.init = function(m) {
    //this.volume_index_store.loadData(m)
    
    var createVolumeButtonHandler = function(m) {
      create_volume(add_new_volume_form.getForm().getValues()['name'], add_new_volume_form.getForm().getValues()['description'], add_new_volume_form.getForm().getValues()['tags'], add_new_volume_form.getForm().getValues()['size']);        
      //Ext.MessageBox.alert('Msg','I will allow this feature at the phase II of preview release. :-) Seung-jin' ); 
    }
    
    add_new_volume_form = new Ext.form.FormPanel({
      //title:"Basic Form",
      monitorValid:true,
      width:425,
      frame:true,
      items: [
         new Ext.form.TextField({ id:"name", fieldLabel:"Name", width:275, allowBlank:false }),
         new Ext.form.TextArea({ id:"description", fieldLabel:"Description", width:275, height:40 }),
         new Ext.form.TextField({ id:"tags", fieldLabel:"Tags", width:275 }),
         new Ext.form.TextField({ id:"size", fieldLabel:"Size (G)", width:40, allowBlank:false, regex: /^0*[1-9][0-9]*$/ })
      ],
      buttons: [ {text:"Create", formBind:true, handler:createVolumeButtonHandler} ],
      buttonAlign: "center"
    });

    add_new_volume_form.render('volume_storage_management');
    
    volume_index_store.loadData({});
    new Ext.grid.GridPanel({
      renderTo: 'volume_storage_management',
      frame: false,
      //title: 'Volume storages' ,
      autoHeight: true ,
      viewConfig: {forceFit: true} ,
      border: false,
      store: volume_index_store ,
      bodyStyle:'margin-top:5px',
      columns: [
        { header: "No", dataIndex: 'no', width: 25, sortable: true},
        { header: "Name", dataIndex: 'name', width: 130, sortable: true } ,
        { header: "Description", dataIndex: 'description', width: 300, sortable: true } ,
        { header: "Tags", dataIndex: 'tags', width: 90, sortable: true, hidden: true } ,
        { header: "Volume id", dataIndex: 'id', width: 90, sortable: true } ,
        { header: "size(G)", dataIndex: 'size', width: 50, sortable: true } ,
        { header: "Snapshot id", dataIndex: 'snapshot_id', width: 100, sortable: true, hidden: true },
        { header: "Status", dataIndex: 'status', width: 80, sortable: true },
        { header: "Create Time" , dataIndex: 'create_time', width: 150, sortable: true },
        { header: "&raquo; Intance id" , dataIndex: 'attach_data_instance_id', width: 100, sortable: true },
        { header: "&raquo; Device" , dataIndex: 'attach_data_device', width: 60, sortable: true },
        { header: "&raquo; Attached time" , dataIndex: 'attach_data_attach_time', width: 150, sortable: true }
      ]
    });
  };

  this.update = function(m) {
    //volume_index_store.loadData(m);
    active_module.add("center.dashboard.volume_storage_grid");
    volume_index_store.loadData((m == null) ? resource_request_jsonstore.getVolumeList : m);
  }
	
}





// authentication keys management
var Keys_grid = function() {
  
  var key_index_store = new Ext.data.JsonStore({
    fields: ["keypair_name","keypair_fingerprint"],
    root: ""
  });
  
  this.init = function(m) {
    key_index_store.loadData({});
    
    add_new_key_form = new Ext.form.FormPanel({
      labelWidth: 80, // label settings here cascade unless overridden
      //url:'save-form.php',
      frame:true,
      layout: 'column',
      //title: 'Simple Form',
      bodyStyle:'padding:1px 1px 1px 1px',
      width: 400,
      defaults: {width: 250},
      defaultType: 'textfield',
      items: [
        {fieldLabel: 'Key pair name', name: 'key_pair_name', allowBlank:false},
        new Ext.Button({ text: 'Issue', boxMaxWidth: 40, handler: function() {
					if (Ext.util.Format.trim(add_new_key_form.getForm().getValues()['key_pair_name']) != "" ) {
            issue_new_key(add_new_key_form.getForm().getValues()['key_pair_name']);
          } else {
            Ext.MessageBox.alert('Notce', "Key name cannot be blank or spaces");
          }
        }})
      ]
    });

    add_new_key_form.render('authentication_keys_management');

    //Ext.DomHelper.append('authentication_keys_management',"" );
    
		
    new Ext.grid.GridPanel({
      renderTo: 'authentication_keys_management',
      frame: false,
      //title: 'Issued keys' ,
      autoHeight: true ,
      bodyStyle:'margin-top:5px',
      viewConfig: {forceFit: true} ,
      border: false,
      store: key_index_store ,
      columns: [
        { header: "Keypair name", dataIndex: 'keypair_name', width: 100, sortable: true},
        { header: "Keypair fingerprint", dataIndex: 'keypair_fingerprint', width: 300, sortable: true },
        //{ header: "Action", dataIndex: 'keypair_name', width: 85, sortable: false, renderer: function(val){ console.log(val); return '<input type="image" src="/site_media/images/cross.png" width="12" alt="Remove" id="delKey" keyname="'+val+'" onClick="console.log(this.keyname)"/>'}}
      	{
			header: "Action",
			dataIndex: 'keypair_name',
			width: 85,
			sortable: false,
			renderer: function(val){ var buttonHTML = '<input type="image" src="/site_media/images/cross.png" width="12" alt="Remove" id="delKey" keyname="'+val+'" onClick="removeKey(\''+val+'\')"/>'; return buttonHTML;} }
			]
    });
   
  }
  
  this.update = function(m) {
    active_module.add("center.dashboard.keys_grid");
    key_index_store.loadData((m == null) ? resource_request_jsonstore.getKeyPairsList : m);
  }
  
}

var removeKey_post = function() {
	ajax_common_gateway("getKeyPairsList", "GET", "", function(){
  		Ext.get('keys_tree').select('*').remove();
  		//var west_cloud_instances = new west.cloud_instances;
			ajax_common_gateway("getKeyPairsListTree", "GET", "", west.foo);
			ajax_common_gateway("getKeyPairsList", "GET", "", keys_grid.update);
		}); // I was a genius two month ago.
}

var issue_new_key = function(key) {
  //console.log(key);
  add_new_key_form.getForm().reset();
  var method_params = "keypair_name=" + key;
	var issuingNewKeyMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Creating your new key. Please wait..."});
	issuingNewKeyMsg.show();
  ajax_common_gateway("createKeyPair", "POST", method_params, function(){
		issuingNewKeyMsg.hide();
  	Ext.get('keys_tree').select('*').remove();
		//var west_cloud_instances = new west.cloud_instances;
		ajax_common_gateway("getKeyPairsListTree","GET","", west.foo);  
		show_key();
  });
}

var show_key = function(k) {
  //console.log(resource_request_jsonstore.createKeyPair);
	tem = resource_request_jsonstore.createKeyPair.split("-----B");
	key_msg = "<pre>-----B"+tem[1]+"</pre>";
  Ext.MessageBox.minWidth = 500;
  Ext.MessageBox.alert('Your root key', key_msg);
  ajax_common_gateway("getKeyPairsListTree","GET","", keys_grid.update);
	ajax_common_gateway("getKeyPairsList", "GET", "", keys_grid.update);
  //console.log(keys_grid);
}

var keys_grid = {"a":"b"};



//////// INIT
////////
////////

var init = function(){
      

  ajax_common_gateway("getVolumeList", "GET", "", function(){});
  
  // ext viewport      
  new Ext.Viewport({
    layout: 'border',
    items: [
        north.init,
        south.init,
        west.init,
        center(),
        east.init
      ]
    });
  
  // Render West trees
  var west_cloud_instances = new west.cloud_instances;
  var west_machine_images = new west.machine_images;
  var west_machine_volumes = new west.machine_volumes;
  var west_authentication_keys = new west.authentication_keys;
  
  // Render CENTER
  
  // Render Launch New Instance accordian
  var launch_new_instance = new Launch_new_instance;
 
  // Render Running instance accordion
  instance_grid = new Instance_grid;
  instance_grid.init();
  
  // Render Machine images management accordion
  machine_image_grid = new Machine_image_grid;
  machine_image_grid.init();

  // Render Volume storage management accordion
  
  volume_storage_grid  = new Volume_storage_grid;
  volume_storage_grid.init();
    
  // Render Authentication keys management accordion
  keys_grid = new Keys_grid;
  keys_grid.init();


	//
  faye_communicator();
  
};

var faye_communicator = function() {
  server = "http://"+window.location.host + ":9000/bayeux";
  channel = "/"+sessionStorage.getItem("userid");
  var client = new Faye.Client(server,{timeout:120});
  var subscription = client.subscribe(channel, function(msgObj) { notice.msg("Notice",msgObj.msg)} );
}  

var notice = function(){
  
 var msgCt;
		function createBox(t, s){
    	return ['<div class="msg">',
            	'<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc"><h3>', t, '</h3>', s, '</div></div></div>',
              '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
              '</div>'].join('');
		}
  
  return {
    	msg : function(title, format){
      console.log(format); 
      //document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/ding_dong.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
      	if(!msgCt){
        	msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
        }
       		msgCt.alignTo(document, 't-t');
          var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
          var m = Ext.DomHelper.append(msgCt, {html:createBox(title, s)}, true);
          m.slideIn('t').pause(4.3).ghost("t", {remove:true});
      }
    };
}();

