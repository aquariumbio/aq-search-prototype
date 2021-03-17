import time

from flask import Flask, render_template, request

from util.sample_search import search_samples, list_samples

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/browser', methods=("GET", "POST"))
def data_browser():
    return render_template('data/browser.html')

@app.route('/samples/search', methods=("GET", "POST"))
def sample_search():
    terms = request.form.get('terms') or ""
    fields = request.form.getlist('fields') or []
    method = request.form.get('method') or 'or'
    debug = None

    if terms:
        results = search_samples(
            terms,
            offset=0,
            limit=20,
            method=method,
            fields=fields
        )
    else:
        results = list_samples(offset=0, limit=20)

    return render_template('samples/search.html', results=results, debug=debug)
