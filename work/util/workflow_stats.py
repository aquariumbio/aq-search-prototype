import sys
import collections
from collections import Counter, defaultdict

import datetime
from datetime import datetime, timedelta, timezone
import dateutil.parser

import statistics
from statistics import median
from itertools import zip_longest

import pytz
from pytz import timezone

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.display.max_rows = 999

import pydent
from pydent import AqSession, models
from pydent.models import Sample, Item, Plan

def get_completed_jobs(operation_type):
    ops = session.Operation.where({"operation_type_id": operation_type.id, 'status': 'done'})
    print("Found {} Operations of type {}".format(len(ops), operation_type.name))

    op_ids = [op.id for op in ops]
    job_associations = session.JobAssociation.where({"operation_id": op_ids})

    job_ids = [ja.job_id for ja in job_associations]
    jobs = session.Job.find(job_ids)
    jobs = [j for j in jobs if j.state[-1]['operation'] == "complete"]
    print("Found {} completed Jobs of type {}".format(len(jobs), operation_type.name))
    
    return jobs

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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def compile_job_data(session, operations):
    ot_data = []

    columns = [
        "n_ops", 
        "start_time", 
        "stop_time", 
        "duration", 
        "length", 
        "job_completeness", 
        "state_completeness", 
        "complete"
    ]
    
    op_type_ids = list(set([o.operation_type_id for o in operations]))
    operation_types = session.OperationType.find(op_type_ids)
    print("Found {} OperationTypes".format(len(operation_types)))

    for operation_type in operation_types:
        ot_id = operation_type.id
        these_operations = [o for o in operations if o.operation_type_id == ot_id]
        jobs = get_job_data(session, these_operations)
        jobs = pd.DataFrame(data=jobs, columns=columns)
        ot_data.append((operation_type, jobs))
        
    return ot_data

def get_job_data(session, operations):
    job_stats = []
    
    op_ids = [op.id for op in operations]
    job_associations = session.JobAssociation.where({"operation_id": op_ids})

    job_ids = list(set([ja.job_id for ja in job_associations]))
    nested_job_ids = chunks(job_ids, 25)        
    jobs = []
    
    for these_job_ids in nested_job_ids:
        jobs += session.Job.find(these_job_ids)
                    
    print("Found {} completed Jobs of type {}".format(len(jobs), operations[0].operation_type.name))
    
    for job in jobs:
        if len(job.state) < 5:
            continue
        js = {}
        js["id"] = job.id
        these_job_associations = [j for j in job_associations if j.job_id == job.id]
        js["n_ops"] = len(these_job_associations)
        js["start_time"] = job.state[2].get('time')
        js["stop_time"] = job.state[-2].get('time')
        
        if js["start_time"] and js["stop_time"]:
            js["duration"] = get_delta((js["start_time"], js["stop_time"]))
            
        js["step_times"] = get_step_times(job.state)
        js["length"] = len([s for s in job.state if s["operation"] == "display"])
        js["job_completeness"] = job.is_complete
        js["state_completeness"] = job.state[-1]['operation']
        js["complete"] = job.is_complete and job.state[-1]['operation'] == "complete"
        job_stats.append(js)
    
    return job_stats

def compile_stats(job_data):
    output_columns = [
        "job_name",
        "num", 
        "mean_time", 
        "median_time", 
        "mean_size", 
        "median_size", 
        "mean_time_per_operation", 
        "median_time_per_operation"
    ]

    output_data = []

    for operation_type, all_data in job_data:
        completed_data = all_data[all_data["complete"]]

        if completed_data.get("duration") is None: continue

        completed_data["time_per_operation"] = completed_data["duration"] / completed_data["n_ops"]
        ax = sns.regplot(x="n_ops", y="duration", data=completed_data)
        ax.set_title(operation_type.name)
        plt.show()

        summary = completed_data.describe()
        output_row = {}
        output_row["job_name"] = operation_type.name
        output_row["num"] = len(completed_data)
        output_row["mean_time"] = summary["duration"]["mean"]
        output_row["median_time"] = summary["duration"]["50%"]
        output_row["mean_size"] = summary["n_ops"]["mean"]
        output_row["median_size"] = summary["n_ops"]["50%"]

        if summary.get("time_per_operation") is not None:
            output_row["mean_time_per_operation"] = summary["time_per_operation"]["mean"]
            output_row["median_time_per_operation"] = summary["time_per_operation"]["50%"]

        output_data.append(output_row)

    output_df = pd.DataFrame(data=output_data, columns=output_columns)
    return output_df

def operations_for_window(session, start, stop):
    window_ops = session.Operation.where("updated_at >= '{}' AND updated_at < '{}'".format(start, stop))
    print("{} Operations found between {} and {}.".format(len(window_ops), start, stop))
    return window_ops