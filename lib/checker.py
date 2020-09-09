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
        self.browser = url_resource.browser
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
        return self.calculate_probability("article", readability_multiplier())


    def video_probability(self):
        '''Probability of a resource being a video'''
        def video_tag_multiplier():
            '''1 if video tag present, else 0'''
            video = self.browser.driver.find_elements_by_tag_name("video")
            if video:
                video = video[0]
                return 1 if self.browser.is_element_medium(video) else 0
            else: return 0
        
        return self.calculate_probability("video", video_tag_multiplier())


    def audio_probability(self):
        '''Probability of a resource being an audio'''
        def audio_tag_multiplier():
            '''1 if audio tag present, else 0'''
            return 1 if self.bs_soup.find("audio") else 0
        return self.calculate_probability("audio", audio_tag_multiplier())


    def image_probability(self):
        '''Probability of a resource containing primarily a image'''
        def image_tag_multiplier():
            '''1 if large/visible image present, else 0'''
            return 1 if self.browser.find_large_visible_images() else 0
        return self.calculate_probability("image", image_tag_multiplier())


    def calculate_probability(self, media_type, curr_res):
        '''Add json-file-media-info and pdf probability to calculation of
           other media probabilities. 
           Args: media_type: type of media to be check in json file
                 curr_res: probability calculated based on DOM'''
        res = (curr_res * 0.6) + (self.json_file_multiplier(media_type) * 0.4) + (self.pdf_probability() * -1)
        return min(1, max(0, round(res, 2)))


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
            return 2 if m == media_type else -0.5
        else:
            return 0.2
