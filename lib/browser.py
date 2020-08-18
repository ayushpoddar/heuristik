from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class Browser():
    """represents the browser"""

    def __init__(self, url = None, mobile = True, headless = True, download_directory = False):
        options = Options()
        options.headless = headless
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36")

        if download_directory:
            options.add_experimental_option('prefs', { 'download.default_directory': str(download_directory) })

        self.driver = webdriver.Chrome(options = options)

        if mobile:
            self.resize_to_mobile()

        if url:
            self.fetch_url(url)


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()


    def resize_to_mobile(self, width = 425, height = 1300):
        """Resize the browser to mobile screen sizes"""
        self.driver.set_window_size(width, height)


    def fetch_url(self, url, sleep_dur = 5):
        """Open a URL in the browser"""
        self.driver.get(url)
        time.sleep(sleep_dur)

    def save_html(self, filename):
        '''Save HTML of the web page'''
        if self.is_webpage_open:
            with open(filename, 'w') as file:
                file.write(self.driver.page_source)

    def save_screenshot(self, filename):
        '''Save screenshot'''
        if self.is_webpage_open:
            self.driver.save_screenshot(filename)

    def is_webpage_open(self):
        '''Returns true if a webpage is open in the browser current window'''
        self.driver.title != ''
