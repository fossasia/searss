# searss
Search to RSS tool

The goal of this mini-tool is gather search results and store it as an RSS feed on a server.

Required Features: 
- A shell script (i.e. python) that reads from stdin a line
- Then it sends this line to e.g. google search as search request. 
- Google responds with the result html.
- The html then is parsed and the search result should be written as stdout in an rss format.
