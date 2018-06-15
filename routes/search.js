var express = require('express');
var router = express.Router();
var http = require('http')
var elasticsearch = require('elasticsearch')

/* The ES client */
var client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'trace'
});


/* GET users listing. */
router.get('/:query', function(req, res, next) {

  client.search({
    index: 'judaicalink',
    type: '_doc',
    body: {
      query: {
        query_string: {
					query: req.params.query
        }
      }
    }
  }).then(function(resp) {
    res.set("Access-Control-Allow-Origin", "*")
    res.json({
      "query": req.params.query,
      "response": resp 
    });
  }, function(err) {
    console.trace(err.message);
  });

});

module.exports = router;
