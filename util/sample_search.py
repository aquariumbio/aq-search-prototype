from util.sample_queries import search_sequential, all_sample_properties, all_samples, count_samples
from util.sample_display import display_list, display_no_results, order

def search_samples(terms, offset=0, limit=20, method='or', fields=[]):
    terms = split(terms)
    samples = search_sequential(terms, fields=fields)
    samples = order(samples, method, n_terms=len(terms))
    n_total = len(samples)
    if samples:
        properties = all_sample_properties([str(s["id"]) for s in samples])
        samples = samples[offset:limit]
        return display_list(samples, properties, n_total, highlight=terms, fields=fields)
    else:
        return display_no_results()

def list_samples(offset=0, limit=20):
    samples = all_samples(offset=offset, limit=limit)
    n_total = count_samples()
    properties = all_sample_properties([str(s["id"]) for s in samples])
    return display_list(samples, properties, n_total)

def split(terms, sep=" "):
    return terms.strip().split(sep)
