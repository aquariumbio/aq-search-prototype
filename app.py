import time

import redis
from flask import Flask, render_template, request

from util.search_prototype import search, list_samples

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/', methods=("GET", "POST"))
def sample_search():
    debug = None
    terms = ""
    fields = []
    method = 'or'

    if request.method == 'POST':
        terms = request.form.get('terms')
        fields = request.form.getlist('fields')
        method = request.form.get('method')
        # debug = method

    if terms:
        results = search(
            terms,
            offset=0,
            limit=20,
            method=method,
            fields=fields
        )
    else:
        results = list_samples(offset=0, limit=20)

    return render_template('search.html', results=results, debug=debug)
