import sys
from bs4 import BeautifulSoup
import requests

def download_and_return():
    r = requests.get('https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html')
    with open('cached.html', 'w') as f:
        f.write(r.text)

    return r.text

def run(to_download=False):
    if to_download:
        html_data = download_and_return()
    else:
        with open('cached.html', 'r') as f:
            html_data = f.read()

    # Parse page and get basic info
    soup = BeautifulSoup(html_data, 'html.parser')
    headers = soup.find_all('h3')
    tables = soup.find_all('table')
    print(f"Num headers: {len(headers)}\nNum tables: {len(tables)}")
    for i in range(len(tables)):
        print(headers[i+2].get('id'))
        print(len(tables[i].find_all('tr')))

    print()

    # Parse all rows.
    i = 0
    rows = tables[0].find_all('tr')
    for row in rows:
        if row.get('class') is not None:
            if row['class'][0] == 'blank-row':
                break
        i += 1
        if i > 100:
            break
        print(row, row.get('class'))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] == "1":
        run(True)
