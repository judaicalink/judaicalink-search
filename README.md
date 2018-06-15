JudaicaLink Search
==================

This is the backend of the JudaicaLink search functionality. It is developed in
node.js and basically takes requests from the JavaScript search.js running on
the client's Webbrowser, passes on the request to ElasticSearch and then
returning the ElasticSearch results back to the browser, where it is displayed.


+----------------------------+    +---------------------------+    +---------------+
|                            |    |                           |    |               |
| Repo: judaicalink-site     |    | Repo: judaicalink+search  |    |               |
| File: static/js/search.js  +----> File: static/js/search.js +----> ElasticSearch |
| Running in the Web browser |    | This backend.             |    |               |
|                            |    |                           |    |               |
|                            |    |                           |    |               |
+----------------------------+    +---------------------------+    +---------------+

## Client (Browser) Code

The browser invokes the search() function that is productively deployed here:

[judaicalink-site:/static/js/search.jd](https://github.com/wisslab/judaicalink-site/blob/master/static/js/search.js)

This function calls the public backend under http://search.judaicalink.org

For development purposes, there is a local version with a corresponding
minimalistic HTML page in the repo:

- [judaicalink-search:/public/js/search.js](https://github.com/wisslab/judaicalink-search/blob/master/public/js/search.js)
- [judaicalink-search:/public/index.html](https://github.com/wisslab/judaicalink-search/blob/master/public/index.html)

If you use a local ElasticSearch, simply change the backend URL there, but
make sure that you change it back to the public URL whenever you copy the code
over to the website!

## This backend 

The main action happens in this file, where requests to /search/:query are
processed.

- [judaicalink-search:/routes/search.js](https://github.com/wisslab/judaicalink-search/blob/master/routes/search.js)

## ElasticSearch

The ElasticSearch server that actually provides the data. The production
version is running on our Web server, but not directly accessible from outside.

You can setup a local version following these instructions: (TODO!)
