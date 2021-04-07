import re
import json

from util.data_queries import find_by_id, io_for, data_associations_for

# An wrapper for Operations that includes methods for collating and reporting metadata.
#
# @author Devin Strickland <strcklnd@uw.edu>
class OperationMap():
    # attr_reader :operation, :predecessor_ids

    def __init__(self, operation):
        self.__operation = operation
        self.__io = None
        self.__inputs = None
        self.__outputs = None
        self.__input_samples = None
        self.__input_parameters = None
        self.__input_data = None
        self.__output_samples = None
        self.__output_data = None
        self.__operation_data = None

    def name(self):
        return self.operation_type()["name"]

    def id(self):
        return self.__operation["id"]

    def operation_type(self):
        return find_by_id("operation_type", self.__operation["operation_type_id"])

    def all_keys(self):
        return sorted(list(set(
            list(self.input_samples().keys()) +
            list(self.input_parameters().keys()) +
            list(self.input_data().keys()) +
            list(self.output_samples().keys()) +
            list(self.output_data().keys()) +
            list(self.operation_data().keys())
        )))

    def fetch_data(self, key):
        data = OperationMap.flatten([
            self.input_samples().get(key),
            self.input_parameters().get(key),
            self.input_data().get(key),
            self.output_samples().get(key),
            self.output_data().get(key),
            self.operation_data().get(key)
        ])
        return [d for d in data if d]

    def io(self):
        if not self.__io:
            self.__io = io_for(self.id())
        return self.__io

    def inputs(self):
        return [x for x in self.io() if x["role"] == "input"]

    def outputs(self):
        return [x for x in self.io() if x["role"] == "output"]

    def input_samples(self):
        if not self.__input_samples:
            self.__input_samples = self.samples_for(self.inputs())
        return self.__input_samples

    def output_samples(self):
        if not self.__output_samples:
            self.__output_samples = self.samples_for(self.outputs())
        return self.__output_samples

    def input_parameters(self):
        if not self.__input_parameters:
            self.__input_parameters = self.parameters_for(self.inputs())
        return self.__input_parameters

    def input_data(self):
        if not self.__input_data:
            self.__input_data = self.data_for(self.inputs())
        return self.__input_data

    def output_data(self):
        if not self.__output_data:
            self.__output_data = self.data_for(self.outputs())
        return self.__output_data

    def operation_data(self):
        if not self.__operation_data:
            data = {}
            self.add_associations(data, "Operation", self.id())
            self.__operation_data = data
        return self.__operation_data

    def item_inputs(self):
        return [i for i in self.inputs() if i["child_item_id"]]

    def item_outputs(self):
        return [o for o in self.outputs() if o["child_item_id"]]

    def output_for(self, item_id):
        fvs = [fv for fv in self.outputs() if fv["child_item_id"] == item_id]
        if fvs: return fvs[0]

    def samples_for(self, field_values):
        samples = {}
        for fv in field_values:
            if not fv["child_sample_id"]: next

            sample = find_by_id('sample', fv["child_sample_id"])
            self.add_data(samples, fv["name"], sample["name"])
        return samples

    def parameters_for(self, field_values):
        parameters = {}
        for fv in field_values:
            if not fv["value"]: next

            if isinstance(fv["value"], dict):
                params = fv["value"]
            else:
                params = { fv["name"]: fv["value"] }

            for key, value in params.items():
                self.add_data(parameters, key, value)
        return parameters

    def data_for(self, field_values):
        data = {}
        for fv in field_values:
            if not fv["child_item_id"]: next

            self.add_associations(data, "Item", fv["child_item_id"])
        return data

    def add_associations(self, hsh, parent_class, parent_id):
        associations = data_associations_for(parent_class, parent_id)
        for association in associations:
            key = association["key"]
            obj = json.loads(association["object"])
            self.add_data(hsh, key, obj[key])

    def add_data(self, hsh, key, value):
        key = self.make_key(key)
        if not hsh.get(key): hsh[key] = []
        hsh[key].append(value)
        return hsh

    def make_key(self, string):
        key = str(string).strip().lower()
        return re.subn(OperationMap.key_replace(), '_', key)[0]

    @classmethod
    def key_replace(cls):
        return re.compile(r"[^a-z0-9?]+")

    @classmethod
    def key_pattern(cls):
        return re.compile(r"[a-z0-9?_]+")

    @classmethod
    def flatten(cls, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return OperationMap.flatten(list_of_lists[0]) + OperationMap.flatten(list_of_lists[1:])
        return list_of_lists[:1] + OperationMap.flatten(list_of_lists[1:])
