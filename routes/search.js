var express = require('express');
var router = express.Router();
var http=require('http')



/* GET users listing. */
router.get('/:query', function(req, res, next) {

	
http.get({
  hostname: 'localhost',
  port: 9200,
  path: '/judaicalink/_search?q=' + req.params.query,
  agent: false  // create a new agent just for this one request
}, (data) => {
  // Do stuff with response
	
data.setEncoding('utf8');
  let rawData = '';
  data.on('data', (chunk) => { rawData += chunk; });
  data.on('end', () => {
    try {
      const parsedData = JSON.parse(rawData);
  	res.set("Access-Control-Allow-Origin", "*") 
	res.json({
		"query": req.params.query, 
		"response": parsedData
	});
    } catch (e) {
      console.error(e.message);
    }
  });
});
});

module.exports = router;
