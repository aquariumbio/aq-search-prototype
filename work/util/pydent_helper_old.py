import sys
import re
import json
import collections
from collections import Counter, defaultdict

import datetime
from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytz
from pytz import timezone
from collections import defaultdict

import pandas as pd
import seaborn as sns

import pydent
from pydent import AqSession, models, __version__
from pydent.models import Sample, Item, Plan

from IPython.core.display import display, HTML


def get_session(instance):
    with open('secrets.json') as f:
        secrets = json.load(f)

    credentials = secrets[instance]
    session = AqSession(
        credentials["login"],
        credentials["password"],
        credentials["aquarium_url"]
    )

    msg = "Connected to Aquarium at {} using pydent version {}"
    print(msg.format(session.url, str(__version__)))

    me = session.User.where({'login': credentials['login']})[0]
    print('Logged in as {}\n'.format(me.name))
    
    return session

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def find_in_batches(model, ids, batch_size):
    n_total = len(ids)
    results = []
    nested_ids = chunks(ids, batch_size)

    for these_ids in nested_ids:
        these_results = model.where({"id": these_ids})
        if these_results:
            results += these_results
            n_found = len(results)
            pct_found = round((100 * n_found / n_total))
            print("Found {}% ({}) of {} records".format(pct_found, n_found, n_total))
            
    return results

def get_delta(times):
    start = dateutil.parser.parse(times[0])
    end = dateutil.parser.parse(times[1])
    return (end - start).seconds/60

def get_step_times(state):
    times = [s["time"] for s in state if s["operation"] == "next"]
    step_times = []
    
    i = 0
    while i < (len(times) - 1):
        step_times.append(get_delta([times[i], times[i+1]]))
        i += 1
    
    return step_times