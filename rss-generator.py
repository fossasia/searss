import mechanize
from feedgen.feed import FeedGenerator
import urlparse
from bs4 import BeautifulSoup


def generateFeed(urls):
    """
    Generates RSS feed from the given urls

    :param urls: List of URL. Each entry contains url, title, short description
    """
    fg = FeedGenerator()
    fg.title('Google Search Results')
    fg.link(href='http://google.com', rel='alternate')
    fg.description('Google Seach Results')
    for url in urls:
        fe = fg.add_entry()
        fe.title(url[0])
        fe.link({'href': url[1], 'rel': 'alternate'})
        fe.description(url[2])
    print fg.rss_str(pretty=True)
    # Write rss feed to file
    # fg.rss_file('rss.xml')


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
        anchor_tag = div.select_one('.r a')
        # Skip if invalid div (it does not contain required a tag)
        if not anchor_tag:
            continue
        # Validate url
        parsed_url = urlparse.urlparse(anchor_tag['href'])
        if 'url' in parsed_url.path:
            url_entry = [anchor_tag.text,
                         urlparse.parse_qs(parsed_url.query)['q'][0],
                         desc[0].text]
            urls.append(url_entry)
    return urls


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


def main():
    query = raw_input("What do you want to search for ? >> ")
    urls = google_search(query)
    generateFeed(urls)


if __name__ == "__main__":
    main()
