import pandas as pd
from util.data_queries import data_for_item
from util.operation_map import OperationMap

def dataframe_for(item_id = None):
    jobs = data_for_item(item_id = item_id)
    reports = []
    for job in jobs:
        operation_reports = []
        for operation in job["operations"]:
            operation_reports.append(report_for(operation))

        reports.append({
            "job_id": job["id"],
            "operations": operation_reports
        })

    return reports

def report_for(operation):
    report = {}
    om = OperationMap(operation)
    report["operation_id"] = om.id()
    report["operation_name"] = om.name()
    report["input_samples"] = om.input_samples()
    report["input_parameters"] = om.input_parameters()
    report["output_samples"] = om.output_samples()
    report["output_items"] = [o["child_item_id"] for o in om.item_outputs()]
    report["input_data"] = om.input_data()
    report["output_data"] = om.output_data()
    report["operation_data"] = om.operation_data()
    return report