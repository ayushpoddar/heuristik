# import requests

# with open('classifier.lua', 'r') as file:
#     script = file.read()

# url = "https://stackoverflow.com/questions/8369219/how-to-read-a-text-file-into-a-string-variable-and-strip-newlines"

# def startRequest():
#     resp = requests.post('http://localhost:8050/execute',
#     json = {
#         'lua_source': script,
#         'url': url
#     })
#     return resp.content

import csv
import browser

csv_file = "url-type.csv"
data_folder = "data/"

urls = []
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        urls.append(row["Url"])

b = browser.Browser()

try:
    for i, url in enumerate(urls):
        print(f"Fetching {url}")
        b.fetch_url(url)
        print("Fetching done")
        b.save_screenshot(data_folder + str(i) + ".png")
        b.save_html(data_folder + str(i) + ".html")
        print(f"Saved data for {url}")
        print(f"Index = {i}\n")
finally:
    print("Closing browser")
    b.driver.quit()

