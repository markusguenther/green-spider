import httpretty
from httpretty import httprettified
import unittest

from checks import textual_content
from checks import page_content
from checks.config import Config

@httprettified
class TestTextualContent(unittest.TestCase):

    def test_links(self):
        self.maxDiff = 2000
        page_body = """
            <html>
                <head>
                    <title>Titel</title>
                </head>
                <body>
                    <p>Hier steht etwas Text der nicht viel <b>Sinn</b> ergibt.</p>
                    <p>Aber es ist ja da so ein Wort.</p>
                </body>
            </html>
        """

        url = 'http://example.com/'
        httpretty.register_uri(httpretty.GET, url, body=page_body)

        results = {}

        config = Config(urls=[url])
        page_content_checker = page_content.Checker(config=config, previous_results={})
        results['page_content'] = page_content_checker.run()

        checker = textual_content.Checker(config=page_content_checker.config,
                                          previous_results=results)
        result = checker.run()
        urls_after = checker.config.urls

        self.assertEqual(result, {
            'http://example.com/': {
                'text': 'steht text sinn ergibt wort',
                'exception': None,
                'stats': {
                    'word_count': 5,
                    'character_count': 23,
                }
            }
        })
        self.assertEqual(urls_after, ['http://example.com/'])


if __name__ == '__main__':
    unittest.main()
