import re
import json

from typing import Dict, List, Pattern
from util.types import FieldValue

from util.data_queries import find_by_id, io_for, data_associations_for


class OperationMap():
    """
    A wrapper for Operations that includes methods for collating and reporting metadata.

    Provides a simplified, standardized interface for getting information about an
    operation. Retrieves the following data types:
        * Samples for all inputs and outputs
        * Input Parameters
        * Data attached to input or output Items
        * Data attached directly to the Operation
    Data structures returned by this class do not recognize differences among these
    types, or differences in capitalization for keys that retrieve them. All keys
    are converted to snake_case. For example, the name of a sample from an input labeled
    'Polymerase' would be added the same list as the value of a DataAssociation with
    the key 'polymerase'. This list would be retrieved using the key 'polymerase'.

    @author Devin Strickland <strcklnd@uw.edu>
    """

    def __init__(self, operation: dict) -> None:
        self.__operation = operation
        self.__io: List[FieldValue] = []
        self.__input_samples: Dict[str, list] = {}
        self.__input_parameters: Dict[str, list] = {}
        self.__input_data: Dict[str, list] = {}
        self.__output_samples: Dict[str, list] = {}
        self.__output_data: Dict[str, list] = {}
        self.__operation_data: Dict[str, list] = {}

    def name(self) -> str:
        """The name of the OperationType"""
        return self.operation_type()["name"]

    def id(self) -> int:
        """The ID of the Operation"""
        return self.__operation["id"]

    def operation_type(self) -> dict:
        """The OperationType"""
        return find_by_id("operation_type",
                          self.__operation["operation_type_id"])

    def all_keys(self) -> List[str]:
        """
        Gets all keys for all types of data associated with the Operation.

        Keys include DataAssociation keys and Operation I/O names. All keys are converted
        to snake_case.
        """
        return sorted(list(set(
            list(self.input_samples().keys()) +
            list(self.input_parameters().keys()) +
            list(self.input_data().keys()) +
            list(self.output_samples().keys()) +
            list(self.output_data().keys()) +
            list(self.operation_data().keys())
        )))

    def fetch_data(self, key: str) -> list:
        """
        Gets all data for a given key that is associated with the Operation.

        The provided key should be in snake_case.
        """
        data = OperationMap.flatten([
            self.input_samples().get(key),
            self.input_parameters().get(key),
            self.input_data().get(key),
            self.output_samples().get(key),
            self.output_data().get(key),
            self.operation_data().get(key)
        ])
        return [d for d in data if d]

    def io(self) -> List[FieldValue]:
        if not self.__io:
            self.__io = io_for(self.id())
        return self.__io

    def inputs(self) -> List[FieldValue]:
        return [x for x in self.io() if x["role"] == "input"]

    def outputs(self) -> List[FieldValue]:
        return [x for x in self.io() if x["role"] == "output"]

    def item_inputs(self) -> List[FieldValue]:
        return [i for i in self.inputs() if i["child_item_id"]]

    def item_outputs(self) -> List[FieldValue]:
        return [o for o in self.outputs() if o["child_item_id"]]

    def input_samples(self) -> Dict[str, List[str]]:
        if not self.__input_samples:
            self.__input_samples = self.collect_samples(self.inputs())
        return self.__input_samples

    def output_samples(self) -> Dict[str, List[str]]:
        if not self.__output_samples:
            self.__output_samples = self.collect_samples(self.outputs())
        return self.__output_samples

    def input_parameters(self) -> Dict[str, list]:
        if not self.__input_parameters:
            self.__input_parameters = self.collect_parameters(self.inputs())
        return self.__input_parameters

    def input_data(self) -> Dict[str, list]:
        if not self.__input_data:
            self.__input_data = self.item_data(self.inputs())
        return self.__input_data

    def output_data(self) -> Dict[str, list]:
        if not self.__output_data:
            self.__output_data = self.item_data(self.outputs())
        return self.__output_data

    def operation_data(self) -> Dict[str, list]:
        if not self.__operation_data:
            data: Dict[str, list] = {}
            self.add_associations(data, "Operation", self.id())
            self.__operation_data = data
        return self.__operation_data

    def collect_samples(self, field_values: List[FieldValue]) -> Dict[str, List[str]]:
        samples: Dict[str, List[str]] = {}
        for fv in field_values:
            if not fv["child_sample_id"]: next

            sample = find_by_id('sample', fv["child_sample_id"])
            self.add_data(samples, fv["name"], sample["name"])
        return samples

    def collect_parameters(self, field_values: List[FieldValue]) -> Dict[str, list]:
        parameters: Dict[str, list] = {}
        for fv in field_values:
            if not fv["value"]: next

            if isinstance(fv["value"], dict):
                params = fv["value"]
            else:
                params = { fv["name"]: fv["value"] }

            for key, value in params.items():
                self.add_data(parameters, key, value)
        return parameters

    def item_data(self, field_values: List[FieldValue]) -> Dict[str, list]:
        data: Dict[str, list] = {}
        for fv in field_values:
            if not fv["child_item_id"]: next

            self.add_associations(data, "Item", fv["child_item_id"])
        return data

    def add_associations(self, obj: dict, parent_class: str, parent_id: int) -> None:
        associations = data_associations_for(parent_class, parent_id)
        for association in associations:
            key = association["key"]
            value = json.loads(association["object"])[key]
            self.add_data(obj, key, value)

    def add_data(self, obj: dict, key: str, value: object) -> None:
        key = self.make_key(key)
        if not obj.get(key): obj[key] = []
        obj[key].append(value)

    @classmethod
    def make_key(cls, string: str) -> str:
        key = str(string).strip().lower()
        return re.subn(OperationMap.key_replace(), '_', key)[0]

    @classmethod
    def key_replace(cls) -> Pattern:
        return re.compile(r"[^a-z0-9?]+")

    @classmethod
    def key_pattern(cls) -> Pattern:
        return re.compile(r"[a-z0-9?_]+")

    @classmethod
    def flatten(cls, list_of_lists: list) -> list:
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return OperationMap.flatten(list_of_lists[0]) + OperationMap.flatten(list_of_lists[1:])
        return list_of_lists[:1] + OperationMap.flatten(list_of_lists[1:])
