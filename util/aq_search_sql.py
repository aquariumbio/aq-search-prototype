import re
from collections import Counter
import pymysql


def get_connection():
    return pymysql.connect(
        host='mysql_db',
        user='aquarium',
        password='aSecretAquarium',
        database='production',
        cursorclass=pymysql.cursors.DictCursor
    )

def search(terms, offset=0, limit=20, method='or'):
    terms = split(terms)
    results = search_sequential(terms)
    results = order(results, method, n_terms=len(terms))
    if results:
        results = results[offset:limit]
        return display_list(results, len(results), highlight=terms)
    else:
        return "## No Results"

def order(results, method, n_terms=None):
    cnt = Counter([r["id"] for r in results]).items()
    if method == 'and' and n_terms:
        cnt = [c for c in cnt if c[1] == n_terms]
    else:
        cnt = sorted(cnt, key=lambda r: r[1], reverse=True)
    return [next(r for r in results if r["id"] == c[0]) for c in cnt]

def search_sequential(terms):
    results = []
    connection = get_connection()
    with connection:
        for term in terms:
            results += select_samples(connection, term)
    return results

def split(terms, sep=" "):
    return terms.split(sep)

def select_samples(connection, term):
    sql = "SELECT DISTINCT samples.*, sample_types.name, users.name " \
          "FROM samples " \
          "JOIN sample_types " \
          "ON sample_types.id = samples.sample_type_id " \
          "JOIN users " \
          "ON users.id = samples.user_id " \
          "JOIN field_values " \
          "ON field_values.parent_id = samples.id " \
          "WHERE field_values.parent_class = 'Sample' " \
          "AND CONCAT (" \
          "sample_types.name, users.name, " \
          "samples.name, samples.description, " \
          "field_values.name, field_values.value" \
          ") REGEXP '{}'".format(term)

    with connection.cursor() as cursor:
        cursor.execute(sql)

    print(sql + "\n")
    return cursor.fetchall()

def display_list(results, total, highlight=None):
    connection = get_connection()
    with connection:
        all_props = all_sample_properties(connection, [str(r["id"]) for r in results])
    text = []

    for result in results:
        these_props = [p for p in all_props if p["parent_id"] == result["id"]]
        text.append(display_entry(result, these_props))

    fulltext = "## Showing {} (of {}) Results".format(len(results), total)
    fulltext += hrule() + hrule().join(text)
    fulltext = re.subn(regexp_from(highlight), highlight_match, fulltext)
    return fulltext[0]

def all_sample_properties(connection, sample_ids):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM field_values " \
              "WHERE parent_class = 'Sample' " \
              "AND parent_id IN ({})".format(",".join(sample_ids))
        cursor.execute(sql)
    return cursor.fetchall()

def all_sample_types(connection, sample_type_ids):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM sample_types " \
              "WHERE id IN ({})".format(",".join(sample_type_ids))
        cursor.execute(sql)
    return cursor.fetchall()

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
    return "{}: {}\n\n".format(name, value)

def regexp_from(terms, oper='|'):
    return re.compile(oper.join(terms), flags=re.IGNORECASE)

def printmd(string):
    display(Markdown(string))

def highlight_match(matchobj):
    return highlight(matchobj.group(0))

def highlight_style():
    return "background-color:yellow;"

def highlight(txt):
    return "<span style=\"{}\">{}</span>".format(highlight_style(), txt)

def color(txt):
    return "<span style=\"color:green;\">{}</span>".format(txt)

def bold(txt):
    return "**{}**".format(txt)

def hrule():
    return "\n\n" + "_"*5 + "\n\n"
