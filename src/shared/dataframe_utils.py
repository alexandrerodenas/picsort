import logging

import pandas as pd


def vertical_concat(a_dataframe: pd.DataFrame, another_dataframe: pd.DataFrame):
    if len(a_dataframe) == len(another_dataframe):
        return pd.concat([a_dataframe, another_dataframe], axis=1)
    else:
        logging.warning("DataFrames lengths do not match.")
