/**
 * The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
 *
 * Project: Atmosphere, iPlant Collaborative
 * Author: Seung-jin Kim
 * Twitter: @seungjin
 * GitHub: seungjin
 *
 **/


var ajax_common_gateway = function(method_name, method_type, method_params, success_callback_function, fail_callback_function) {

  //if (!method_name) { }
  //if (!method_type) { }
  //if (!method_params) { }
  if (!success_callback_function) { success_callback_function = function() { }; console.log("success callback function does not exit. ajax_common_gateway") }
  if (!fail_callback_function) { fail_callback_function = function() { }; }
  
  Ext.Ajax.request({
    url : '/resource_request/' + method_name , 
    method: method_type,
    params : method_params,
    success: function ( result, request ) { 
      //Ext.MessageBox.alert('Success', 'Data return from the server: '+ result.responseText);
      try { var resultJson = JSON.parse(result.responseText) }
      catch (err) {
        Ext.MessageBox.alert('Request failed', result.responseText);
        //success_callback_function();
      }
      sessionStorage.setItem("__"+method_name,JSON.stringify(resultJson));
      switch(resultJson.result.code)
      {
          case "success":
            eval("resource_request_jsonstore."+method_name+" = resultJson.result.value");
            success_callback_function();
            break;
          case "systemTrouble":
            Ext.MessageBox.alert('System trouble', "system trouble");
            break;
          case "fail":
            eval("resource_request_jsonstore."+method_name+" = resultJson.result.value");
            fail_callback_function();
            break;
          default:
            Ext.MessageBox.alert('API Server does not like you', "API SERVER returns api call with return code value = fail");
       }
    },
    failure: function (result, request) {
      Ext.MessageBox.alert('Failed', result.responseText); 
    } 
  })
}
