import unittest

from lxml import etree
from xmlunittest import XmlTestCase

rssgen = __import__("rss-generator")


class TestGoogleSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availability(self):

        print "Testing for Google Availablity"
        result, code = rssgen.get_results_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):

        print "Testing for Google Search"
        url = rssgen.google_search(self.query)
        self.assertIsNotNone(len(url))


class TestBingSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availability(self):

        print "Testing for Bing Availablity"
        result, code = rssgen.get_bing_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):

        print "Testing for Bing Search"
        url = rssgen.bing_search(self.query)
        self.assertIsNotNone(len(url))


class TestDuckduckgoSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availablity(self):

        print "Testing for duckduckgo Availablity"
        result, code = rssgen.get_duckduckgo_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):

        print "Testing for duckduckgo Search"
        url = rssgen.duckduckgo_search(self.query)
        self.assertIsNotNone(len(url))


class TestAskcomSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availablity(self):

        print "Testing for Ask.com Availablity"
        result, code = rssgen.get_askcom_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):

        print "Teting for Ask.com Search"
        url = rssgen.askcom_search(self.query)
        self.assertIsNotNone(len(url))


class TestFeedGenerator(XmlTestCase):

    query = "FOSSASIA"
    sampleUrlDictionary = [["FOSSASIA | Asia's Open Technology "
                            "Organization for Open Source ...",
                            "https://fossasia.org/",
                            "FOSSASIA Open Tech Community - Open Source, Big Data,"
                            " Design Thinking \nand Free Knowledge Tools with Asia's Premier Open"
                            " Technology Organization."]]
    testTitle = 'GOOGLE SEARCH RESULTS'
    testDescription = 'Google search results for FOSSASIA'
    testLink = 'htps://www.google.com'
    testDocs = 'http://www.rssboard.org/rss-specification'
    testGenerator = 'python-feedgen'

    def test_XMLValidity(self):

        print "Testing for Validity of XML Response recieved."
        xmlFeed = rssgen.generateFeed(self.sampleUrlDictionary, self.query, 0).encode("utf-8")
        self.assertIsNotNone(xmlFeed)
        self.assertXmlDocument(xmlFeed)

    def test_NameSpaceValidity(self):

        print "Testing existance of Namaspaces atom,content"
        xmlFeed = rssgen.generateFeed(self.sampleUrlDictionary, self.query, 0)
        root = self.assertXmlDocument(xmlFeed)
        self.assertXmlNamespace(root, 'atom', 'http://www.w3.org/2005/Atom')
        self.assertXmlNamespace(root, 'content', 'http://purl.org/rss/1.0/modules/content/')

    def test_ElementsValidity(self):

        print "Testing Validity of title,description,lastBuildDate,link,docs,generator tags"
        xmlFeed = rssgen.generateFeed(self.sampleUrlDictionary, self.query, 0)
        root = etree.fromstring(xmlFeed)
        channel = root.find('channel')
        title = channel.find('title')
        description = channel.find('description')
        link = channel.find('link')
        lastBuildDate = channel.find('lastBuildDate')
        docs = channel.find('docs')
        generator = channel.find('generator')
        self.assertXmlNode(title, tag='title', text=self.testTitle)
        self.assertXmlNode(description, tag='description', text=self.testDescription)
        self.assertXmlNode(link, tag='link', text=self.testLink)
        self.assertXmlNode(lastBuildDate, tag='lastBuildDate')
        self.assertXmlNode(docs, tag='docs', text=self.testDocs)
        self.assertXmlNode(generator, tag='generator', text=self.testGenerator)


if __name__ == '__main__':
    test_classes = [TestGoogleSearch, TestBingSearch, TestDuckduckgoSearch, TestAskcomSearch, TestFeedGenerator]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
