import time

import redis
from flask import Flask

from util.search_prototype import search

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def sample_search():
    terms = "norn unfolded singer"
    results = search(terms, offset=0, limit=20, method='or')
    return results