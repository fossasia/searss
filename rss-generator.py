
DESC = """
The goal of this mini-tool is gather search results and store it as an RSS feed on a server.
"""
ASCII = """
 _______  _______  _______  ______    _______  _______ 
|       ||       ||   _   ||    _ |  |       ||       |
|  _____||    ___||  |_|  ||   | ||  |  _____||  _____|
| |_____ |   |___ |       ||   |_||_ | |_____ | |_____ 
|_____  ||    ___||       ||    __  ||_____  ||_____  |
 _____| ||   |___ |   _   ||   |  | | _____| | _____| |
|_______||_______||__| |__||___|  |_||_______||_______|

"""

import mechanize
from feedgen.feed import FeedGenerator
import urlparse
import requests
from bs4 import BeautifulSoup
import sys
import argparse
from argparse import RawTextHelpFormatter


google_feed = ("GOOGLE SEARCH RESULTS", "htps://www.google.com",
               "Google search results for %s")
duckduckgo_feed = ("DUCKDUCKGO SEARCH RESULTS",
                   "htps://www.duckduckgo.com", "Duckduckgo search results for %s")
bing_feed = ("BING SEARCH RESULTS", "https://www.bing.com",
             "Bing search results for %s")


def generateFeed(urls, query, search_engine):
    """
    Generates RSS feed from the given urls

    :param urls: List of URL. Each entry contains url, title, short description
    :param feed_title: Title of the feed
    :param feed_link: Link of the feed
    :param feed_descr: Short description of feed
    """
    # google as search engine
    if search_engine == 0:
        feed = google_feed
    # duckduckgo as search engine
    elif search_engine == 1:
        feed = duckduckgo_feed
    elif search_engine == 2:
        feed = bing_feed

    fg = FeedGenerator()
    fg.title(feed[0])
    fg.link(href=feed[1], rel='alternate')
    fg.description(feed[2] % query)

    for url in urls:
        fe = fg.add_entry()
        fe.title(url[0])
        fe.link({'href': url[1], 'rel': 'alternate'})
        fe.description(url[2])
    print fg.rss_str(pretty=True)
    # Write rss feed to file
    # fg.rss_file('rss.xml')


def get_results_page(query):
    """
    Fetch the google search results page

    :param query:   String to be searched on Google
    :return:        Result page containing search results
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)  # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open('http://www.google.com/')
    br.select_form(name='f')
    br.form['q'] = query
    return br.submit()


def get_duckduckgo_page(query):
    """
    Fetch the duckduckgo search results page

    :param query:   String to be searched on duckduckgo
    :return:        Result page containing search results
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)  # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open('http://www.duckduckgo.com/html/')
    br.select_form(name='x')
    br.form['q'] = query
    return br.submit()


def get_bing_page(query):
    """
    Fetch the bing search results page
    :param query:   String to be searched on bing
    :return:        Result page containing search results
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)  # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open('http://www.bing.com/search')
    formcount = 0
    for form in br.forms():
        if str(form.attrs["id"]) == "sb_form":
            break
        formcount += 1
    br.select_form(nr=formcount)
    br.form['q'] = query
    return br.submit()


def google_search(query):
    """
    Search google for the query and return set of urls
    :param query:   String to be searched
    :return:        List of results. Each entry contains Title, URL,
                    Short description of the result
    """
    urls = []
    response = get_results_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')   # using html5lib parser
    # Search for all relevant 'div' tags with class 'g'
    for div in soup.find_all('div', class_='g'):
        # Search for 'span' containing the short description
        desc = div.find_all('span', class_='st')
        # Search for 'a' containing the link
        try:
            anchor_tag = div.h3.a
        except:
            # Skip if invalid div (it does not contain required a tag)
            continue

        # Validate url
        parsed_url = urlparse.urlparse(anchor_tag['href'])
        if 'url' in parsed_url.path:
            url_entry = [anchor_tag.text,
                         urlparse.parse_qs(parsed_url.query)['q'][0],
                         desc[0].text]
            urls.append(url_entry)
    return urls


def duckduckgo_search(query):
    """
    Search google for the query and return set of urls
    :param query:   String to be searched
    :return:        List of results. Each entry contains Title, URL,
                    Short description of the result
    """
    urls = []
    response = get_duckduckgo_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')
    # Search for all relevant 'div' tags with having the results
    for div in soup.findAll('div', attrs={'class': ['result', 'results_links', 'results_links_deep', 'web-result']}):
        # search for title
        title = div.h2.text.replace("\n", '').replace("  ", "")
        # get anchor tag having the link
        url = div.h2.a['href']
        # get the short description
        desc = div.find('a', attrs={'class': 'result__snippet'}).text
        url_entry = [title, url, desc]
        urls.append(url_entry)
    return urls


def bing_search(query):
    """
    Search bing for the query and return set of the urls

    :param query:   String to be searched
    :return:        List of results. Each entry contains Title, URL,
                    Short description of the result
    """
    urls = []
    response = get_bing_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')

    # Search for all relevant 'div' tags with having the results
    for li in soup.findAll('li', attrs={'class': ['b_algo']}):
        # search for title
        title = li.h2.text.replace("\n", '').replace("  ", "")
        # get anchor tag having the link
        url = li.h2.a['href']
        # get the short description
        desc = li.find('p').text
        url_entry = [title, url, desc]
        urls.append(url_entry)
    return urls


def main():

    """
    A smart argument parser to efficiently sort arguments 
    and raise errors properly. Argument parser is scalable.
    """

    parser = argparse.ArgumentParser(
        description='\n{}\n{}\n'.format(ASCII,DESC), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--google', action='store_true',
                        help='Set search engine as Google')
    parser.add_argument('--bing', action='store_true',
                        help='Set search engine as Bing')
    parser.add_argument('--duckduckgo', action='store_true',
                        help='Set search engine as DuckDuckGo')
    parser.add_argument('-q','--query', action='store', dest='query',
                        help='Specify search query. eg : --query "xkcd comics"')
    args = parser.parse_args()

    if args.google: #If Google is passed as argument
        if args.query: #If query is passed as argument
            query = args.query
            urls = google_search(query)
        else:
            query = raw_input("What do you want to search for ? >> ")
            urls = google_search(query)
        generateFeed(urls, query, 0)

    elif args.duckduckgo: #If DuckDuckGo is passed as argument
        if args.query: #If query is passed as argument
            query = args.query
            urls = duckduckgo_search(query)
        else:
            query = raw_input("What do you want to search for ? >> ")
            urls = duckduckgo_search(query)
        generateFeed(urls, query, 1)

    elif args.bing: #If Bing is passed as argument
        if args.query: #If query is passed as argument
            query = args.query
            urls = bing_search(query)
        else:
            query = raw_input("What do you want to search for ? >> ")
            urls = bing_search(query)
        generateFeed(urls, query, 2)

    else: #If no arguments or wrong arguments are passed
        search_engine = int(raw_input(
            "Select the search engine (0 for google / 1 for duckduckgo / 2 for bing): "))
        if search_engine not in [0, 1, 2]:
            print("Wrong choice. Please enter a valid choice.")
            main()

        query = raw_input("What do you want to search for ? >> ")

        
        if search_engine == 0:  # Google Search
            urls = google_search(query)
            generateFeed(urls, query, search_engine)
        
        elif search_engine == 1: # DuckDuckGo Search
            urls = duckduckgo_search(query)
            generateFeed(urls, query, search_engine)

        elif search_engine == 2: # Bing Search
            urls = bing_search(query)
            generateFeed(urls, query, search_engine)


if __name__ == "__main__":
    main()
