/**
 * The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
 *
 * Project: Atmosphere, iPlant Collaborative
 * Author: Seung-jin Kim
 * Twitter: @seungjin
 * GitHub: seungjin
 *
 **/

var Launch_new_instance = function() {
  active_module.add("center.dashboard.launch_new_instance");
  var image_id_store = new Ext.data.JsonStore({
    fields: [ 'image_name', 'image_description', 'image_tags', 'image_id',
      'image_location', 'image_ownerid', 'image_state', 'image_is_public',
      'image_product_codes', 'image_architecture', 'image_type', 'image_ramdisk_id', 'image_kernel_id',
      {name:'aa', mapping: 'image_id + " (" + obj.image_name + ")" '}
    ],
    root: "",
    data: [{}]
  })

  var vm_types_store = new Ext.data.JsonStore({
    fields: ['name','cpus', 'memory', 'disc', {name:'aa', mapping: 'name + " (Cpu: " + obj.cpus + ", Mem: " + obj.memory + "M, Disk: " + obj.disc + "G)" '}],
    root: "",
    data: [{}]
  });

  var auth_key_store = new Ext.data.JsonStore({
    fields: ['keypair_name', 'keypair_fingerprint'],
    root: "",
    data: [{}]
  });
 
  // I dont use this for now
  var volume_store = new Ext.data.JsonStore({
    fields: [ 'no', 'id', 'size', 'snapshot_id', 'status', 'create_time', 'attach_data_instance_id', 'attach_data_device', 'attach_data_attach_time' ],
    root: "",
    data: [{}]
  })
  volume_store.addListener("expand",function() {alert("ss");});
  
  var instance_name_textinput = { fieldLabel: 'Instance name', name: 'instance_name', allowBlank: false };
  
  var image_id_combobox = new Ext.form.ComboBox({
    store: image_id_store,
    fieldLabel: 'Image id',
    hiddenName: 'image_id',
    displayField: 'aa',
    valueField: 'image_id',
    typeAhead: true,
    mode: 'local',
    triggerAction: 'all',
    emptyText:'Select image...',
    selectOnFocus:true,
    editable:false,
    allowBlank: false
  });
  image_id_combobox.addListener("expand",function() {
		var loadingImgListMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Loading Image Catalog. Please wait..."});
		loadingImgListMsg.show();
		ajax_common_gateway("getImageList", "GET", "", function(m){loadingImgListMsg.hide(); image_id_store.loadData(resource_request_jsonstore.getImageList);});});
  
  var instance_size_combobox = new Ext.form.ComboBox({
    store: vm_types_store,
    fieldLabel: 'Instance size',
    hiddenName: 'instance_size',
    displayField: 'aa',
    valueField: 'name',
    typeAhead: true,
    mode: 'local',
    triggerAction: 'all',
    emptyText:'Select instance size...',
    selectOnFocus:true,
    vtyle: 'email',
    editable:false,
    allowBlank: false
  })
  instance_size_combobox.addListener("expand",function() {ajax_common_gateway("getVmTypes", "GET", "", function(m){vm_types_store.loadData(resource_request_jsonstore.getVmTypes);});});
  
  var authentication_key_combobox = new Ext.form.ComboBox({
    store: auth_key_store,
    fieldLabel: 'Authentication key',
    hiddenName: 'auth_key',
    displayField: 'keypair_name',
    typeAhead: true,
    mode: 'local',
    triggerAction: 'all',
    emptyText:'Select auth key...',
    selectOnFocus:true,
    editable:false,
    allowBlank: true
	})
  authentication_key_combobox.addListener("expand",function() {
		var authKeyLoadingMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Loading your key info. Please wait..."});
		authKeyLoadingMsg.show();
		ajax_common_gateway("getKeyPairsList", "GET", "", function(m){authKeyLoadingMsg.hide(); auth_key_store.loadData(resource_request_jsonstore.getKeyPairsList);});});
  
  var number_of_instance_combobox = {
    fieldLabel: 'Number of instances',
    name: 'num_of_instances',
    emptyText:'1'
  };

  var lifetime_inputbox = {
    fieldLabel: 'Lifetime (Hours)',
    name: 'instance_lifetime',
    emptyText:'0'
  };
  
  var description_textarea = new Ext.form.TextArea({
		fieldLabel: 'Description',
		name: 'instance_description',
		selectOnFocus:true,
		height:120
	});

  var tag_textinput = {
    fieldLabel: 'Tags (Comma separated)',
    name: 'instance_tags'
    //emptyText:'Tag your instance'
  };

  var launch_pad = new Ext.FormPanel({
    labelWidth: 120, // label settings here cascade unless overridden
    //url:'/resource_request/launchInstance',
    frame:true,
    title: 'Create new instance',
    method: 'POST',
    bodyStyle:'padding:5px 5px 0',
    width: 470,
    defaults: {width: 300},
    defaultType: 'textfield',
    items: [
      instance_name_textinput,
      image_id_combobox,
      instance_size_combobox,
      authentication_key_combobox, 
      number_of_instance_combobox,
      lifetime_inputbox,
      description_textarea,
      tag_textinput
    ],
    buttons: [{
        text: 'Launch',
        handler: function(){
          
          if ( launch_pad.getForm().isValid() ) {
            //console.log(launch_pad.getForm().getFieldValues());
            auth_key = launch_pad.getForm().getFieldValues().auth_key;
            image_id = launch_pad.getForm().getFieldValues().image_id;
            instance_description = launch_pad.getForm().getFieldValues().instance_description;
            //EJS - not sure if 'inatance_name' is referenced elsewhere, but for now, it seems innocuous
            inatance_name = launch_pad.getForm().getFieldValues().instance_name;
            instance_size = launch_pad.getForm().getFieldValues().instance_size;
            instance_lifetime = launch_pad.getForm().getFieldValues().instance_lifetime;
            instance_tags = launch_pad.getForm().getFieldValues().instance_tags;
            num_of_instances = launch_pad.getForm().getFieldValues().num_of_instances;
            
            //var ajax_common_gateway = function(method_name, method_type, method_params, success_function) {
						
						var launchingVmMsg = new Ext.LoadMask(Ext.getBody(), {msg:"Launching your VM. Please wait..."});
						launchingVmMsg.show();

      /*
       ajax_common_gateway("launchInstance", "POST", launch_pad.getForm().getFieldValues(), function(m) { 
							Ext.MessageBox.alert('Status', 'Instance booting succeed.<br/>Please wait a few minutes to access. [code1]');
      */
      
      /* 
      ajax_common_gateway("launchApp", "POST", launch_pad.getForm().getFieldValues(),
       success_callback_function = function(m){
        Ext.MessageBox.alert('Status', 'Instance booting succeed.<br/>Please wait a few minutes to access. [code1]');
        launchingVmMsg.hide();
							launch_pad.getForm().reset();
      },
      fail_callback_function = function() {
        launchingVmMsg.hide();
        launch_pad.getForm().reset();
        document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/doh.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
        a = JSON.parse(sessionStorage.getItem("__launchApp")).result.value;
        Ext.MessageBox.alert('Message', "<b><font color='#408080'>Your quota is over.</font></b><br/>Current resource use: "+a.current_cpu+" cpu, "+a.current_mem+"M mem<br/>Quota : "+a.limit_cpu+" cpu, "+a.limit_mem+"M mem");
      }
    );
      */
       ajax_common_gateway("launchInstance", "POST", launch_pad.getForm().getFieldValues(),
       success_callback_function = function(m){
        Ext.MessageBox.alert('Status', 'Instance booting succeed.<br/>Please wait a few minutes to access. [code1]');
        launchingVmMsg.hide();
							launch_pad.getForm().reset();
      },
      fail_callback_function = function() {
        launchingVmMsg.hide();
        launch_pad.getForm().reset();
        //document.getElementById("dummy").innerHTML="<embed src=\"/site_media/sounds/doh.wav\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
        a = JSON.parse(sessionStorage.getItem("__launchInstance")).result.value;
        Ext.MessageBox.alert('Message', "<b><font color='#408080'>Your quota is over.</font></b><br/>Current resource use: "+a.current_cpu+" cpu, "+a.current_mem+"M mem<br/>Quota : "+a.limit_cpu+" cpu, "+a.limit_mem+"M mem");
      }
    );
       
     
              
          } else {
            //console.log("lacunh_pad.getForm().isValid() returns false");
            Ext.MessageBox.alert('Alert', 'Invalid Inputs');
          }
          
          /*
          if ( launch_pad.getForm().isValid() ) {
            launch_pad.getForm().submit(
              {
                method: "POST",
                waitMsg: 'Launching new instance...',
                success: function(f,a) {
                  Ext.MessageBox.alert('Status', 'Instance booting succeed.<br/>Please wait a few minutes to access. [code1]');
                  launch_pad.getForm().reset();
                },
                failure: function(f,a) {
                  if (a.failureType === Ext.form.Action.CONNECT_FAILURE){
                    Ext.MessageBox.alert('Status', 'Instance launching failure. Please try again later');
                  }
                  if (a.failureType === Ext.form.Action.SERVER_INVALID){
                    //Ext.Msg.alert('Warning', a.result.errormsg);
                    // FOR NOW
                    Ext.MessageBox.alert('Status', 'Instance booting succeed.<br/>Please wait a few minutes to access. [code2]');
                    launch_pad.getForm().reset();
                  }
                }
              });
          } else {
            Ext.MessageBox.alert('Alert', 'Invalid inputs');  
          }
          
          */
          
          
        }
      }]
    });

  launch_pad.render('launch_new_instance');

};

// detacheVolume
var detachVolume = function(f) {
  
  //var a = f.id + '_selected_volume_detach';
  //selected_volume = document.getElementById(a.substring(15)).value;
  //console.log(f.id.substring(14));
  instance_id = f.id.substring(14);
  var a = f.id.substring(14)+"_selected_volume_detach";
  selected_volume = document.getElementById(a).value;
  
  Ext.Ajax.request({
      url: '/resource_request/detachVolume' ,
      method: 'POST' , 
      params: {
        instance_id : instance,
        volume_id : selected_volume
      },
      success: function( result, request ) {
        //inst_info_json = Ext.util.JSON.decode(result.responseText);
        Ext.MessageBox.alert('Notice', "Detached");
      } ,
      failure: function( result, request ) { Ext.MessageBox.alert('Failed', 'Detaching failed'); }
  })
}

var create_volume = function(name,desc,tags,size) {
  //resource_request seungjin 1d78108e-74ed-41bf-8be3-4b9bd441186a POST http://bond.iplantcollaborative.org:8000/resources/v1/createVolume "size=10&name=test&description=a&tags=b"
  param = "size=" + size+ "&name=" + name + "&description=" + desc + "&tags=" + tags;
  //ajax_common_gateway("createVolume", "POST", param, fooC)
  ajax_common_gateway("createVolume", "POST", param,
    success_callback_function = function() {
      console.log(sessionStorage.getItem("__createVolume"));
      console.log(eval("("+sessionStorage.getItem("__createVolume")+")").result.value[0]);
      Ext.MessageBox.alert('Alert', "Volume "+eval("("+sessionStorage.getItem("__createVolume")+")").result.value[0]+" was created.");
      add_new_volume_form.getForm().reset();
      
    },
    fail_callback_function = function() {
      //
      console.log("create_volume_failed");
      console.log(m);
      Ext.MessageBox.alert('Failed', 'Not attached. Not valid volume');
    }
  );
}

var attachVolume = function(f) {
  var a = f.id + '_selected_volume';
  selected_volume = document.getElementById(a.substring(15)).value;
  var b = 'selected_device_' + f.id.substring(15);
  selected_device = document.getElementById(b).value;
  
  Ext.Ajax.request({
    url: '/resource_request/attachVolume' ,
    method: 'POST' , 
    params: {
      instance_id : instance,
      volume_id : selected_volume,
      device: selected_device
    },
    success: function( result, request ) {
      //inst_info_json = Ext.util.JSON.decode(result.responseText);
      Ext.MessageBox.alert('Alert', "Attached!");
    } ,
    failure: function( result, request ) { Ext.MessageBox.alert('Failed', 'Not attached. Not valid volume'); }
  })
};


var removeKey = function(key_name) {
	var method_params = "keypair_name=" + key_name;
	ajax_common_gateway("removeKeyPair","POST",method_params,removeKey_post);
};

