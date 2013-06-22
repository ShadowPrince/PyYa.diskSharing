import http.client
import urllib.parse
import re
import json
import socket
import sys
from html.parser import HTMLParser

"""
Get direct link from shortlink (yadi.sk/XxXxX), provided via first argument.
Direct link not bounded to IP, but it is temporary.
"""

# simple html parser for our needs
# find data, that passes [validator] fn and in [tag]
class Parser(HTMLParser):
    def __init__(self, tag, validator):
        self.inside = False
        self.tag = tag
        self.validator = validator
        self.result = None
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if self.tag == tag:
            self.inside = True

    def handle_endtag(self, tag):
        if self.tag == tag:
            self.inside = False

    def handle_data(self, data):
        if self.inside and self.validator(data):
            self.result = data

# return body of download page
def get_download_page(hash):
    connection = http.client.HTTPConnection('disk.yandex.ru')
    try:
        connection.request('GET', '/public/?hash=%s' % hash, '')
        return connection.getresponse().read().decode('utf-8')
    except socket.gaierror:
        raise RuntimeError('Can\'t open download page!')

# return JS code of download page
def get_js_code(page):
    parser = Parser('script', lambda x: x.startswith('$.extend'))
    parser.feed(page)
    if parser.result:
        return parser.result
    else:
        raise RuntimeError('Download page is invalid!')

# parse and return JSON params of second argument $.extend call (ckey is there)
def get_json(js_code):
    r = re.search('^\$\.(?P<window>[^{]+)(?P<json>.+)\)', js_code)
    try:
        return json.loads(r.group('json'))
    except ValueError:
        raise RuntimeError('JS from download page is invalid!')

# return direct link 
def get_direct_link(hash, ckey):
    connection = http.client.HTTPConnection('disk.yandex.ru')
    try:
        connection.request(
                'POST', 
                '/handlers.jsx', 
                urllib.parse.urlencode({
                    '_ckey': ckey,
                    '_name': 'getLinkFileDownload',
                    'hash': hash,
                    }),
                {'Content-Type': 'application/x-www-form-urlencoded'})
        data = json.loads(
                connection.getresponse().read().decode('utf-8')
                )
        if not data.get('success', False):
            raise RuntimeError('Error: ' + str(data))

        return data.get('data', {}).get('url', None)
    except (socket.gaierror, ValueError):
        raise RuntimeError('disk.yandex.ru/handlers.jsx return wrong response:' + str(data))

# get file hash from url
def get_hash(url):
    urlp = urllib.parse.urlparse(url)
    if urlp.netloc == 'yadi.sk':
        connection = http.client.HTTPConnection(urlp.netloc)
        try:
            connection.request('GET', urlp.path)
            parser = Parser('a', lambda x: True)
            parser.feed(connection.getresponse().read().decode('utf-8'))
            if parser.result:
                return get_hash(parser.result)
            else:
                raise RuntimeError('Download page invalid!')
        except socket.gaierror:
            raise RuntimeError('Failed to open download page!')
    elif urlp.netloc.startswith('disk.yandex'):
        r = re.search('^hash\=(.*)$', urlp.query)
        return urllib.parse.unquote(r.group(1))

if __name__ == '__main__':
    try:
        hash = get_hash(sys.argv[1])
        ckey = get_json(
                get_js_code(
                    get_download_page(hash))).get('Disk', {}).get('Page', {}).get('ckey', None)

        print(get_direct_link(hash, ckey))
    except IndexError:
        print('LINK argument not provided!')
    except Exception as e:
        raise e
