// The contents of this file are subject to the terms listed in the LICENSE file you received with this code.

/*
  Author: Seung-jin Kim
  Email: seungjin@email.arizona.edu
  Twitter: @seungjin
*/



var faye = require('./lib/faye-node');
ENDPOINT = 'http://localhost:9000/bayeux';
var client = new faye.Client(ENDPOINT);

target = "/"+process.ARGV[2]
message = process.ARGV[3]

client.publish(target,{"msg":message},function(){   });

setTimeout(function() { process.exit(); }, 500);
