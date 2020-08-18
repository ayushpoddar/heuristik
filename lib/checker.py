from bs4 import BeautifulSoup
from readability import Document

class Checker():
    """Check a URL Resource for various types of media"""
    min_article_length = 1000
    bs_parser = "lxml"

    def __init__(self, url_resource):
        self.url_resource = url_resource
        self.html = url_resource.html

        if self.html.is_file():
            with open(self.html, "r") as file:
                self.bs_soup = BeautifulSoup(file, self.bs_parser)
                self.decompose_soup()
                self.readability_doc = Document(str(self.bs_soup))

    def decompose_soup(self):
        for ele in self.bs_soup.find_all(["script", "link"]):
            ele.decompose()

    def is_pdf_downloaded(self):
        """Check if a PDF has been downloaded"""
        if list(self.url_resource.folder.glob('*.pdf')):
            return True
        else:
            return False

    def is_article(self):
        """Check if the URL resource is an article"""
        if self.is_pdf_downloaded():
            return False  # No need to check if PDF is downloaded
        else:
            readability_soup = BeautifulSoup(self.readability_doc.summary(), self.bs_parser)
            text = " ".join([s for s in readability_soup.stripped_strings])
            text = " ".join(text.split())
            return len(text) > self.min_article_length
