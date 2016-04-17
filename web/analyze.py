#!/usr/bin/env python
'''
'''
import os
import sys

from flask import Flask, abort, jsonify, request

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib import analyze_bt5156_url


app = Flask(__name__)

def gen_url(api='api', ver='v0.1', task='analyze'):
    return '/%s/%s/%s' % (api, ver, task)

@app.route(gen_url(), methods=['POST'])
def do_analyze():
    if not request.json or 'url' not in request.json:
        abort(400)
    url = request.json['url']
    return jsonify(analyze_bt5156_url.analyze(url)), 200

if __name__ == '__main__':
    app.run(debug=True)
