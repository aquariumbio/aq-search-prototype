from time import perf_counter

from flask import Flask, render_template, request

from util.sample_search import search_samples, list_samples
from util.data_browser import dataframe_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/browser', methods=("GET", "POST"))
def data_browser():
    item_id = request.form.get('item') or None
    tables = []
    debug = None

    if item_id:

        df = dataframe_for(item_id = item_id)
        # tables=[df.to_html(classes='data')]

        tables = [df]

    return render_template('data/browser.html',
                           tables=tables,
                           debug=debug)

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
