"""
Extracts natural text from a page
"""

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from bs4 import BeautifulSoup

from checks.abstract_checker import AbstractChecker

class Checker(AbstractChecker):
    def __init__(self, config, previous_results=None):
        super().__init__(config, previous_results)

        # Load stopwords from nltk, add our own
        self.stop_words = set(stopwords.words('german'))
        self.stop_words.add("ja")
    
    def run(self):
        assert 'page_content' in self.previous_results
        
        results = {}

        for url in self.config.urls:
            results[url] = self.get_text(url)

        return results
    
    def get_text(self, url):
        """
        Parse page content and return text without stopwords
        """
        page_content = self.previous_results['page_content'][url]
        assert 'content' in page_content

        if page_content['content'] is None:
            return

        result = {
            'text': "",
            'stats': {},
            'exception': None,
        }

        soup = BeautifulSoup(page_content['content'], 'html.parser')

        text = soup.body.text.strip()
        text = text.lower()

        word_tokens = word_tokenize(text)
        
        filtered_sentence = []
        for w in word_tokens:
            if w in self.stop_words:
                continue
            if w in (".", ",", ";", "?", ":", "!"):
                continue

            filtered_sentence.append(w)

        result['text'] = " ".join(filtered_sentence)
        result['stats'] = {
            'word_count': len(filtered_sentence),
            'character_count': len("".join(filtered_sentence)),
        }

        return result
