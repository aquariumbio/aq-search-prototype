from collections import Counter
import re

def display_list(samples, properties, n_total, highlight=None, fields=[]):
    highlight = regexp_from(highlight)
    text = []
    for sample in samples:
        these_props = [p for p in properties if p["parent_id"] == sample["id"]]
        text.append(display_entry(sample, these_props, highlight, fields))

    fulltext = "<h2>Showing {} (of {}) Results</h2>".format(len(samples), n_total)
    fulltext += hrule() + hrule().join(text)
    return fulltext

def display_entry(sample, properties, highlight, fields):
    disp = display_property(sample["id"], highlight_by_regex(highlight, sample["name"]))
    disp += display_property("Description", highlight_by_regex(highlight, sample["description"]))

    sample_type = sample["sample_types.name"]
    if 'sample_type' in fields: sample_type = highlight_by_regex(highlight, sample_type)
    disp += display_property("Sample Type", sample_type)

    owner_name = sample["users.name"]
    if 'owner' in fields: owner_name = highlight_by_regex(highlight, owner_name)
    disp += display_property("Owner", owner_name)

    for p in properties:
        value = p["value"]
        if value and 'properties' in fields:
            value = highlight_by_regex(highlight, value)

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

def highlight_by_regex(regex, txt):
    return re.subn(regex, highlight_match, txt)[0]

def highlight_match(matchobj):
    return highlight(matchobj.group(0))

def highlight_style():
    return "background-color:yellow;"

def highlight(txt):
    return "<span class=\"highlight\">{}</span>".format(txt)

def color(txt):
    return "<span class=\"user-defined\">{}</span>".format(txt)

def bold(txt):
    return "<b>{}</b>".format(txt)

def hrule():
    return "<hr>"

def display_no_results():
    return "<h2>No Results</h2>"
