import csv
import fetcher

csv_file = "url-type.csv"

urls = []
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        url = row["Url"]
        m_type = row["Type"]
        urls.append([url, m_type])

for i in range(30, len(urls)):
    url = urls[i][0]
    m_type = urls[i][1]
    a = fetcher.main(url)
    print(url)
    print("------------------------------------------------------")
    print("Required type:", m_type.lower(), "|", "Got:", a)
    print("======================================================")

