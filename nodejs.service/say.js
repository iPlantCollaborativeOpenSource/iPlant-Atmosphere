var faye = require('./lib/faye-node');
ENDPOINT = 'http://localhost:9000/bayeux';
var client = new faye.Client(ENDPOINT);

target = "/"+process.ARGV[2]
message = process.ARGV[3]

client.publish(target,{"msg":message},function(){   });

setTimeout(function() { process.exit(); }, 500);
