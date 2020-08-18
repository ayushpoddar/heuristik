import browser, sys, uuid, checker, shutil
from pathlib import Path

class URLResource():
    """fetch a given URL"""
    project_dir = Path('/Users/ayushpoddar/Documents/workspace/heuristik')

    def __init__(self, url):
        self.url = url
        self.folder = self.project_dir / uuid.uuid4().hex
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
        self.attributes = checker.Checker(self).media_type_info()
        return self.attributes

    def remove_folder(self):
        shutil.rmtree(self.folder)


with URLResource(sys.argv[1]) as r:
    r.get_url()
    a = r.get_attributes()
    print(a)

