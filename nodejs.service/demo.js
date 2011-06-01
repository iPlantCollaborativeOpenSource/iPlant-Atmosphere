var faye = require('./lib/faye-node');
var http = require('http');
var client = new faye.Client('http://localhost:9000/faye');
client.publish("/a","asdasdasdasd");
