import time

from flask import Flask, render_template, request

from util.search_prototype import search, list_samples

app = Flask(__name__)

@app.route('/', methods=("GET", "POST"))
def sample_search():
    terms = request.form.get('terms') or ""
    fields = request.form.getlist('fields') or []
    method = request.form.get('method') or 'or'
    debug = None

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
