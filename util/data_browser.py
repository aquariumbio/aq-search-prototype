import pandas as pd
from functools import reduce
from util.data_queries import data_for_item
from util.operation_map import OperationMap

def reports_for(item_id = None):
    jobs = data_for_item(item_id = item_id)
    reports = []
    for job in jobs:
        operation_reports = []
        for operation in job["operations"]:
            operation_reports.append(report_for(operation))

        operation_name = operation_reports[0].get("operation_name")

        columns = [r.pop("data_keys", []) for r in operation_reports]
        columns = reduce(lambda x, y: x+y, columns)
        columns = sorted(list(set(columns)))
        columns = ["operation_id", "output_items"] + columns
        data = [r.pop("data", {}) for r in operation_reports]
        dataframe = pd.DataFrame(columns = columns, data = data)

        reports.append({
            "job_id": job["id"],
            "operation_name": operation_name,
            "operations": operation_reports,
            "dataframe": dataframe
        })

    return reports

def report_for(operation):
    om = OperationMap(operation)
    report = {}
    report["data_keys"] = om.all_keys()
    report["operation_name"] = om.name()

    data = {}
    data["operation_id"] = om.id()
    output_items = [o["child_item_id"] for o in om.item_outputs()]
    data["output_items"] = join(output_items)
    for key in report["data_keys"]:
        this_data = om.fetch_data(key)
        data[key] = join(this_data)

    report["data"] = data
    return report

def join(iterable):
    return ", ".join([str(x) for x in iterable])