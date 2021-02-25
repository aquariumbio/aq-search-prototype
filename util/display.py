from collections import Counter
import re

def display_list(samples, properties, n_total, highlight=None):
    text = []
    for sample in samples:
        these_props = [p for p in properties if p["parent_id"] == sample["id"]]
        text.append(display_entry(sample, these_props))

    fulltext = "<h2>Showing {} (of {}) Results</h2>".format(len(samples), n_total)
    fulltext += hrule() + hrule().join(text)
    fulltext = re.subn(regexp_from(highlight), highlight_match, fulltext)
    return fulltext[0]

def display_entry(sample, properties):
    disp = display_property(sample["id"], sample["name"])
    disp += display_property("Sample Type", sample["sample_types.name"])
    disp += display_property("Owner", sample["users.name"])
    disp += display_property("Description", sample["description"])
    for p in properties:
        if p["value"]:
            disp += display_property(p["name"], p["value"], True)
        elif p["child_sample_id"]:
            value = "Sample {}".format(p["child_sample_id"])
            disp += display_property(p["name"], value, True)
    return disp

def display_property(name, value, user_defined=False):
    name = bold(name)
    if user_defined: name = color(name)
    return "<p>{}: {}</p>".format(name, value)

def order(samples, method, n_terms=None):
    cnt = Counter([s["id"] for s in samples]).items()
    if method == 'and' and n_terms:
        cnt = [c for c in cnt if c[1] == n_terms]
    else:
        cnt = sorted(cnt, key=lambda c: c[1], reverse=True)
    return [next(s for s in samples if s["id"] == c[0]) for c in cnt]

def regexp_from(terms, oper='|'):
    return re.compile(oper.join(terms), flags=re.IGNORECASE)

def highlight_match(matchobj):
    return highlight(matchobj.group(0))

def highlight_style():
    return "background-color:yellow;"

def highlight(txt):
    return "<span style=\"{}\">{}</span>".format(highlight_style(), txt)

def color(txt):
    return "<span style=\"color:green;\">{}</span>".format(txt)

def bold(txt):
    return "<b>{}</b>".format(txt)

def hrule():
    return "<hr>"

def display_no_results():
    return "<h2>No Results</h2>"
