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
    type: 'doc',
    body: {
      query: {
        match: {
          _all: req.params.query
        }
      }
    }
  }).then(function(resp) {
    var hits = resp.hits.hits;
    res.set("Access-Control-Allow-Origin", "*")
    res.json({
      "query": req.params.query,
      "response": parsedData
    });
  }, function(err) {
    console.trace(err.message);
  });

});

module.exports = router;
