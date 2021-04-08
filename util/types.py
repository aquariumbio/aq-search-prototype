from typing import TypedDict

class FieldValue(TypedDict, total=False):
    id: int
    parent_id: int
    value: str
    child_sample_id: int
    child_item_id: int
    name:str
    parent_class: str
    role: str
    field_type_id: int
    row: int
    column: int
    allowable_field_type_id: int