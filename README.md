# searss
Search to RSS tool

The goal of this mini-tool is gather search results and store it as an RSS feed on a server.

# Requirements
* Python 2
* [PIP](https://pip.pypa.io/en/stable/installing/)
* [Mechanize](http://wwwsearch.sourceforge.net/mechanize/)
* [Feedgen](https://github.com/lkiesow/python-feedgen)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

# Installing
Install requirements using `pip install -r requirements.txt`

# Using
Run `python rss-generator.py` and enter the search query. A RSS feed will be displayed containing the search results.
