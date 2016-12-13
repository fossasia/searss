from feedgen.feed import FeedGenerator
import requests
from bs4 import BeautifulSoup

SEARCH_ENDPOINT = "https://duckduckgo.com/html/"

# python 2 and 3 compatibility for input function
try:
   input = raw_input
except NameError:
   pass


def generateFeed(results):
    ''' Generates RSS feel from the given urls '''
    fg = FeedGenerator()
    fg.title('DuckDuckGo Search Results')
    fg.link(href='http://duckduckgo.com', rel='alternate')
    fg.description('DuckDuckGo Seach Results')
    for result in results:
        fe = fg.add_entry()
        fe.title(result['title'])
        fe.link({'href': result['item_url'], 'rel':'alternate'})
    print(fg.rss_str(pretty=True))



def get_search_results(query, limit = 10):
        resp = requests.get(SEARCH_ENDPOINT, params ={'q':query})
        soup = BeautifulSoup(resp.content,'html5lib')
        results = soup.findAll('div',attrs={'class':['result','results_links','results_links_deep','web-result']})
        meta_list = []

        for result in results[:limit]:
                try:
                        meta = {}
                        meta['title'] = result.h2.text.replace("\n",'').replace("  ","")
                        meta['item_url'] = result.h2.a['href']
                        # meta['subtitle'] = result.find('a',attrs={'class':'result__snippet'}).text
                        # meta['thumbnail'] = 'http:' + result.img['src']
                        meta_list.append(meta)
                except:
                        pass
        return meta_list


def main():
    query = input("What do you want to search for ? >> ")
    results = get_search_results(query)
    generateFeed(results)

if __name__ == "__main__":
    main()
