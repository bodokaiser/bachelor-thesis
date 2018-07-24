var http = require('http')
var bone = require('bonescript')

const PIN = 'P8_15'

bone.pinMode(PIN, 'out')
bone.digitalWrite(PIN, 1)

http.createServer(function(req, res) {
  bone.digitalWrite(PIN, 0)

  setTimeout(function() {
    bone.digitalWrite(PIN, 1)

    res.end('OK')
  }, 1)
}).listen(6200)
