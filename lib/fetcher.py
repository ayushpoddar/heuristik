import browser, checker, defaults
import sys, uuid, shutil, urllib.parse
import selenium.common.exceptions

class URLResource():
    """fetch a given URL"""

    def __init__(self, url):
        self.update_url_info(url)
        self.folder = defaults.project_dir / uuid.uuid4().hex
        self.html = self.folder / "scrap.html"
        self.folder.mkdir(exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.remove_folder()


    def update_url_info(self, url):
        '''Update variables associated with the url of the resource'''
        self.url = url
        self.url_parts = urllib.parse.urlsplit(url)
        self.domain = self.url_parts.hostname


    def do_the_thing(self):
        """Opens the URL and gets the attributes"""
        with browser.Browser(download_directory=self.folder, mobile=False) as b:
            self.browser = b
            new_url = b.fetch_url(self.url)
            b.save_html(self.html)
            # In case of redirects, the URL in the address bar can be different
            # from the one originally supplied.
            if new_url != self.url:
                self.update_url_info(new_url)

            return self.get_attributes()


    def get_attributes(self):
        """Create a attributes dict describing the nature of media type"""
        check_obj = checker.Checker(self)
        if self.html.is_file():
            self.attributes = {
                "pdf": check_obj.pdf_probability(),
                "article": check_obj.article_probability(),
                "video": check_obj.video_probability(),
                "audio": check_obj.audio_probability(),
                "image": check_obj.image_probability()
            }
        else:
            self.attributes = None
        return self.attributes


    def remove_folder(self):
        shutil.rmtree(self.folder)


def main(url):
    with URLResource(url) as r:
        try:
            a = r.do_the_thing()
            return a
        except selenium.common.exceptions.WebDriverException as e:
            print(e)
            return {}


if __name__ == "__main__":
    a = main(sys.argv[1])
    print(a)
