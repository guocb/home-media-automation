#!/usr/bin/env python
'''
'''
import argparse
import json
import sys
import re
import urllib

from contextlib import closing


def analyze(url):
    with closing(urllib.urlopen(url)) as page:
        html = page.read()
    m = re.search('var thunder_url = "(.+?)";', html)
    rc = {}
    if not m:
        return {'result': 'error',
                'message': 'Cannot find xunlei link in the URL!'}

    return {'result': 'OK', 'message': 'found the link',
            'link': m.group(1).decode('gbk').encode('utf-8')}

def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-u', '--url', required=True,
                        help='The page url of bbs.bt5156.net')
    return parser.parse_args(argv)

def main(argv):
    opts = parse_args(argv)
    print json.dumps(analyze(opts.url))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
