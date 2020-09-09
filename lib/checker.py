from bs4 import BeautifulSoup
from readability import Document
import json
import defaults

class Checker():
    """Check a URL Resource for various types of media"""
    min_article_length = 1000
    bs_parser = "lxml"

    with open(defaults.domain_info_file_path) as f:
        '''Load the JSON file containing info on the type of content
           expected in any particular domain'''
        domain_info = json.load(f)

    def __init__(self, url_resource):
        self.url_resource = url_resource
        if url_resource.html.is_file():
            with open(url_resource.html, "r") as file:
                self.bs_soup = BeautifulSoup(file, self.bs_parser)
                self.decompose_soup()
                self.readability_doc = Document(str(self.bs_soup))

    def decompose_soup(self):
        for ele in self.bs_soup.find_all(["script", "link"]):
            ele.decompose()

    def pdf_probability(self):
        """1 if a PDF has been downloaded, else 0"""
        return 1 if list(self.url_resource.folder.glob('*.pdf')) else 0

    def article_probability(self):
        """Probability of a resource being an article"""
        def readability_multiplier():
            """1 if the readability parser detects substantial length of text, else 0"""
            readability_soup = BeautifulSoup(self.readability_doc.summary(), self.bs_parser)
            text = " ".join([s for s in readability_soup.stripped_strings])
            text = " ".join(text.split())
            return int(len(text) > self.min_article_length)
        res = (readability_multiplier() * 0.5) + (self.json_file_multiplier("article") * 0.5) + \
                                               (self.pdf_probability() * -1)
        return max(0, res)


    def media_type_from_domain(self):
        domain = self.url_resource.domain
        if domain in self.domain_info:
            return self.domain_info[domain].lower()
        else:
            return None


    def json_file_multiplier(self, media_type):
        '''Return the multiplier factor obtained via json file info'''
        m = self.media_type_from_domain()
        if m:
            return 1 if m == media_type else -0.5
        else:
            return 0.75
