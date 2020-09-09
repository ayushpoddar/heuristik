import browser, checker, defaults
import sys, uuid, shutil, urllib.parse

class URLResource():
    """fetch a given URL"""

    def __init__(self, url):
        self.url = url
        self.url_parts = urllib.parse.urlsplit(url)
        self.domain = self.url_parts.hostname
        self.folder = defaults.project_dir / uuid.uuid4().hex
        self.html = self.folder / "scrap.html"
        self.folder.mkdir(exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.remove_folder()

    def get_url(self):
        """Get URL"""
        with browser.Browser(download_directory=self.folder) as b:
            b.fetch_url(self.url)
            b.save_html(self.html)

    def get_attributes(self):
        """Create a attributes dict describing the nature of media type"""
        check_obj = checker.Checker(self)
        if self.html.is_file():
            self.attributes = {
                "pdf": check_obj.is_pdf_downloaded(),
                "article": check_obj.is_article()
            }
        else:
            self.attributes = None

        return self.attributes

    def remove_folder(self):
        shutil.rmtree(self.folder)


with URLResource(sys.argv[1]) as r:
    r.get_url()
    a = r.get_attributes()
    print(a)

