import time

import redis
from flask import Flask, render_template

from util.search_prototype import search

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/', methods=("GET", "POST"))
def sample_search():
    terms = "norn unfolded singer"
    results = search(terms, offset=0, limit=20, method='or')
    return render_template('search.html', results=results)
