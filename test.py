import unittest

rssgen = __import__("rss-generator")


class TestGoogleSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availability(self):

        print("Testing for Google Availablity")
        result, code = rssgen.get_results_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):

        print("Testing for Google Search")
        url = rssgen.google_search(self.query)
        self.assertIsNotNone(len(url))


class TestBingSearch(unittest.TestCase):

    query = "FOSSASIA"

    def test_availability(self):

        print("Testing for Bing Availablity")
        result, code = rssgen.get_bing_page(self.query)
        self.assertEqual(code, 200)

    def test_search(self):
    	print("Testing for Bing Search")
        url = rssgen.bing_search(self.query)
        self.assertIsNotNone(len(url))


class TestDuckduckgoSearch(unittest.TestCase):

	query = "FOSSASIA"

	def test_availablity(self):

		print("Testing for duckduckgo Availablity")
		result,code = rssgen.get_duckduckgo_page(self.query)
		self.assertEqual(code,200)

	def test_search(self):

		print("Testing for duckduckgo Search")
		url=rssgen.duckduckgo_search(self.query)
		self.assertIsNotNone(len(url))

class TestAskcomSearch(unittest.TestCase):

	query = "FOSSASIA"

	def test_availablity(self):

		print("Testing for Ask.com Availablity")
		result,code = rssgen.get_askcom_page(self.query)
		self.assertEqual(code,200)

	def test_search(self):

		print("Teting for Ask.com Search")
		url = rssgen.askcom_search(self.query)
		self.assertIsNotNone(len(url))


if __name__ == '__main__':
    test_classes = [TestGoogleSearch, TestBingSearch, TestDuckduckgoSearch,TestAskcomSearch]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
