#!env/bin/python

import json
import urllib.request

URL = 'https://md1-a.akamaihd.net/sitesearch-api/search.jsonp?query=e&sort=displaydatetime+desc&startat={}'
OUTPUT_FILENAME = 'output.csv'

def open_json_url(url):
    return json.loads(urllib.request.urlopen(url).read().decode())

def get_article_urls(data):
    return [doc['contenturl'] for doc in data['results']['documents']]

# loop
## open url
## save contents to file

def scrape(url, number, fd):
    count = 0
    while count < number:
        urls = get_article_urls(open_json_url(url.format(count)))
        count += len(urls)
        fd.write(''.join(map(
            lambda a: a + '\n',
            urls
        )))
    return count

if __name__ == '__main__':
    # Input
    import argparse
    parser = argparse.ArgumentParser(description='Scrape urls from a webpage')
    parser.add_argument('output_filename', metavar='output file', nargs='?',
                        help='File to output counts to')
    output_filename = parser.parse_args().output_filename or OUTPUT_FILENAME

    number = int(open_json_url(URL.format(0))['results']['total'])
    with open(output_filename, 'w') as fd:
        count = scrape(URL, number, fd)
    print("Found {} urls".format(count))
