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


    def resize_to_mobile(self, width = 425, height = 900):
        """Resize the browser to mobile screen sizes"""
        self.driver.set_window_size(width, height)


    def fetch_url(self, url, sleep_dur = 5):
        """Open a URL in the browser
           Return the window's current URL (useful in case of redirects)"""
        self.driver.get(url)
        time.sleep(sleep_dur)
        return self.driver.current_url


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


    def window_height(self):
        '''Get height of window'''
        return self.driver.get_window_size()['height']


    def element_height(self, elem):
        '''Return height of the given element'''
        script = '''
                    var ele = arguments[0];
                    return ele.offsetHeight;
                '''
        return self.driver.execute_script(script, elem)


    def element_y_pos(self, elem):
        '''Get the y-position of the element in the DOM'''
        script = "var ele = arguments[0]; return ele.getBoundingClientRect().top;"
        return self.driver.execute_script(script, elem)


    def is_element_large(self, elem):
        '''Check if the element is large enough'''
        return self.is_element_x_size(0.6)(elem)


    def is_element_medium(self, elem):
        '''Check if element is medium in size'''
        return self.is_element_x_size(0.3)(elem)


    def is_element_x_size(self, ratio):
        '''Return a one argument function that takes an element as argument
           and returns if it has the minimum height as compared to the window
           height. This minimum height is defined by the ratio'''
        def helper(elem):
            return int(self.element_height(elem)) >= ratio * self.window_height()
        return helper


    def find_all_images(self):
        '''Returns all images'''
        return self.driver.find_elements_by_tag_name('img')


    def is_element_visible(self, elem):
        '''If the given element is visible in the top viewport or not'''
        # script = '''var ele = arguments[0];
        #             var box = ele.getBoundingClientRect();
        #             var cx = box.left + box.width / 2;
        #             var cy = box.top + box.height / 2;
        #             var e = document.elementFromPoint(cx, cy);
        #             for (; e; e = e.parentElement) {
        #                 if (e === ele)
        #                     return true;
        #             }
        #             return false;'''
        # return self.driver.execute_script(script, elem)
        return self.element_y_pos(elem) < 0.6 * self.window_height()


    def find_large_visible_images(self):
        '''Find large and visible images'''
        filter_fn = lambda ele: self.is_element_visible(ele) and self.is_element_large(ele)
        return list(filter(filter_fn, self.find_all_images()))
