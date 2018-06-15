search = function() {
  var BACKEND_DEV = "http://localhost:3000"
  var BACKEND_PROD = "http://search.judaicalink.org"

  /* CHANGE THIS TO BACKEND_PROD BEFORE DEPLOYING! */
  var backend = BACKEND_DEV

  var query = $("#query").val()
  if (query.trim().length == 0) {
    console.log("Empty query")
    return
  }
  console.log("Query: " + JSON.stringify(query))

  var updateResults = function(query, pageNumber, cb) {

    $.getJSON(backend + "/search/" + pageNumber + "/" + query, function(data) {
      // console.log(data)		
      var total = data.response.hits.total
      var hits = data.response.hits.hits.length
      var h = $("#results")
      h.html("<p>Total Hits: " + total + "</p>")
      h.append("<p>First " + hits + " hits:</p>")
      var reslist = $("<ol></ol>").appendTo(h)
      for (i = 0; i < hits; i++) {
        var result = data.response.hits.hits[i]
        reslist.append("<li><a href='" + result["_id"] + "'>" + result["_source"].name + "</a> (Score: " + result["_score"] + ")</li>")
      }
      if (typeof cb === 'function') {
				cb(total)
			}
    })
  }

  updateResults(query, 1, function(total) {

    $("#pagination").pagination({
      items: total,
      itemsOnPage: 10,
      cssStyle: 'light-theme',
      onPageClick: function(pageNumber) {
        updateResults(query, pageNumber)
      }
    });
  })


}
