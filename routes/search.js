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
router.get('/:page/:query', function(req, res, next) {
  var page = parseInt(req.params.page)
  if (page <= 0) {
    page = 1
  }
  client.search({
    index: 'judaicalink',
    type: '_doc',
    from: (page - 1) * 10,
    size: 10,
    body: {
      query: {
				query_string: {

          query: req.params.query,
          fields: ["name^4", "Alternatives^3", "birthDate", "birthLocation^2", "deathDate", "deathLocation^2", "Abstract", "Publication"]
        }

      },
      highlight: {
        fields: {
          "name": {},
          "Alternatives": {},
          "birthDate": {},
          "birthLocation": {},
          "deathDate": {},
          "deathLocation": {},
          "Abstract": {},
          "Publication": {}
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
