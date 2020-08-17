import browser, sys, uuid, checker, shutil
from pathlib import Path

class URLResource():
    """fetch a given URL"""
    project_dir = Path('/Users/ayushpoddar/Documents/workspace/heuristik')

    def __init__(self, url):
        self.url = url
        self.folder = self.project_dir / uuid.uuid4().hex
        self.html = self.folder / "scrap.html"

    def get_url(self):
        """Get URL"""
        try:
            self.folder.mkdir(exist_ok = True)
            b = browser.Browser(download_directory=self.folder)
            b.fetch_url(self.url)
            b.save_html(self.html)
        finally:
            b.driver.quit()

    def get_attributes(self):
        checker_obj = checker.Checker(self)
        checker_obj.build_attributes()
        print(checker_obj.attributes)

    def remove_folder(self):
        shutil.rmtree(self.folder)



resource = URLResource(sys.argv[1])
resource.get_url()
try:
    resource.get_attributes()
finally:
    resource.remove_folder()

