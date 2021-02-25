from util.search import split, search_sequential, all_sample_properties
from util.display import display_list, display_no_results, order

def search(terms, offset=0, limit=20, method='or'):
    terms = split(terms)
    samples = search_sequential(terms)
    samples = order(samples, method, n_terms=len(terms))
    n_total = len(samples)
    if samples:
        properties = all_sample_properties([str(s["id"]) for s in samples])
        samples = samples[offset:limit]
        return display_list(samples, properties, n_total, highlight=terms)
    else:
        return display_no_results()


