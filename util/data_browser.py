import pandas as pd
from util.data_queries import data_for_item

def dataframe_for(item_id = None):
    df = data_for_item(item_id = item_id)
    return df