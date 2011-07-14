/**
 * The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
 *
 * Project: Atmosphere, iPlant Collaborative
 * Author: Seung-jin Kim
 * Twitter: @seungjin
 * GitHub: seungjin
 *
 **/

var east = {
	init :{
				region: 'east',
        title: 'Properties',
        collapsible: true,
        collapsed: true,
        split: true,
        width: 225, // give east and west regions a width
        minSize: 175,
        maxSize: 400,
        margins: '0 5 0 0',
        layout: 'fit', // specify layout manager for items
        items: new Ext.TabPanel({
          border: false, // already wrapped so don't add another border
          activeTab: 0, 
          tabPosition: 'bottom',
          items: [
            new Ext.grid.PropertyGrid({
              title: 'User information',
              source: {
                "Username": sessionStorage.getItem("userid"),
                "Institution": "",
                "Department" : "iPlant Collaborative",
                "API Ver": "v1",
                "WEB UI Ver": 0.01,
                "Session timeout" : "Token based",
                "Interface style" : "Gray",
                "API Token" : sessionStorage.getItem("token"),
                "API Server" : sessionStorage.getItem("api_server"),
                "Ec2 Access Key" : sessionStorage.getItem("ec2_access_key"),
                "Ec2 Secret Key" : sessionStorage.getItem("ec2_secret_key"),
                "Ec2 URL" : sessionStorage.getItem("ec2_url"),
                "S3 URL" : sessionStorage.getItem("s3_url"),
                "API Server" : sessionStorage.getItem("api_server"),
                "Quota/CPU (Unit)" : sessionStorage.getItem("quota_cpu"),
                "Quota/MEM (Mega)" : sessionStorage.getItem("quota_mem")
              }
            }),
            {
              html: '<p>Serivce at this panel is not open yet.</p>',
              title: 'Settings',
              closable: true,
              autoScroll: true
            }
          ]
        })
      },	
	foo : function() { return "I am foo"; }
	
}
