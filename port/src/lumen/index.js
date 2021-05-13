// vortex lumen web app
const path = require('path');
var express = require('express');
var app = express();

app.use(express.static(__dirname));
app.get('/', function(req, res){
    res.sendFile('/opt/lumen/html/index.html');
});
    
app.listen(3000);
