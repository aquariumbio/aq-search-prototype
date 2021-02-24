import re
from collections import Counter
import pymysql
from IPython.display import Markdown, display


def get_connection():
    return pymysql.connect(
        host='mysql_db',
        user='aquarium',
        password='aSecretAquarium',
        database='production',
        cursorclass=pymysql.cursors.DictCursor
    )

def split(terms, sep=" "):
    return terms.split(sep)

def regexp_from(terms, oper='|'):
    terms = split(terms)
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

def order(results):
    ids = [r["id"] for r in results]
    cnt = sorted(Counter(ids).items(), key=lambda r: r[1], reverse=True)
    return [next(r for r in results if r["id"] == c[0]) for c in cnt]

def hrule():
    return "\n\n" + "_"*5 + "\n\n"

def select_samples(term):
    sql = "SELECT DISTINCT samples.* " \
          "FROM samples JOIN field_values " \
          "ON field_values.parent_id = samples.id " \
          "WHERE field_values.parent_class = 'Sample' " \
          "AND (" \
          "samples.name REGEXP '{}' " \
          "OR samples.description REGEXP '{}' " \
          "OR field_values.name REGEXP '{}' " \
          "OR field_values.value REGEXP '{}')".format(term, term, term, term)
        
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    
    print(sql + "\n")
    return cursor.fetchall()

def search_sequential(terms):
    terms = split(terms)
    results = []
    for term in terms:
        results += select_samples(term)
    return results
    
def search(terms, limit=20):
    results = search_sequential(terms)
    return [order(results)[:limit], len(results)]

def all_sample_properties(sample_ids):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM field_values " \
                  "WHERE parent_class = 'Sample' " \
                  "AND parent_id IN ({})".format(",".join(sample_ids))
            cursor.execute(sql)
    return cursor.fetchall()

def display_property(name, value, user_defined=False):
    name = bold(name)
    if user_defined: name = color(name)
    return "{}: {}\n\n".format(name, value)

def display_entry(sample, properties):
    disp = "{} {}\n\n".format(bold(sample["id"]), sample["name"])
    disp += display_property("Description", sample["description"])
    for p in properties:
        if p["value"]:
            disp += display_property(p["name"], p["value"], True)
        elif p["child_sample_id"]:
            value = "Sample {}".format(p["child_sample_id"])
            disp += display_property(p["name"], value, True)
    return disp
    
def display_list(results, total, highlight=None):
    all_props = all_sample_properties([str(r["id"]) for r in results])
    text = []
    
    for result in results:
        these_props = [p for p in all_props if p["parent_id"] == result["id"]]
        text.append(display_entry(result, these_props))
        
    fulltext = "## Showing {} (of {}) Results".format(len(results), total) 
    fulltext += hrule() + hrule().join(text)
    fulltext = re.subn(regexp_from(highlight), highlight_match, fulltext)
    printmd(fulltext[0])