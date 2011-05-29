var fs    = require('fs'),
    path  = require('path'),
    sys   = require('sys'),
    http  = require('http'),
    faye  = require('./lib/faye-node');

var PUBLIC_DIR = path.dirname(__filename) + '/public',
    bayeux     = new faye.NodeAdapter({mount: '/bayeux', timeout: 20}),
    port       = process.ARGV[2] || '9000';

var server = http.createServer(function(request, response) {
		response.writeHead(200, {'Content-Type': 'text/html'});
    response.write('');
    response.end();
/*
  var path = (request.url === '/') ? '/index.html' : request.url;
  fs.readFile(PUBLIC_DIR + path, function(err, content) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(content);
    response.end();
  });
*/
});

bayeux.attach(server);
server.listen(Number(port));

sys.puts('Listening on ' + port);


