import logging
import json
import pandas as pd
import numpy as np
import warnings

from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
def tickerStreamPart1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = to_cumulative(inputValue)
    # logging.info("My result :{}".format(result))
    logging.info("My result :{}".format(result))
    return json.dumps(result)




def to_cumulative(stream: list):
    list_clean = []
    for i in stream:
        list_clean.append(list(i.split(",")))

    df = pd.DataFrame.from_records(list_clean)

    UniqueTicker = df[1].unique()

    DataFrameDict = {elem: pd.DataFrame() for elem in UniqueTicker}

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df[1] == key]

    for key in DataFrameDict.keys():
        DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
        DataFrameDict[key][3] = DataFrameDict[key][3].astype(float)
        DataFrameDict[key]['notional'] = DataFrameDict[key][2] * DataFrameDict[key][3]
        DataFrameDict[key]['cum_qty'] = DataFrameDict[key][2].cumsum()
        DataFrameDict[key]['cum_not'] = DataFrameDict[key]['notional'].cumsum()

    df_new = pd.concat(DataFrameDict.values(), ignore_index=True)
    df_new.sort_values(by=[0], inplace=True)
    # print(df_new)

    unique_timestamp = df_new[0].unique()

    DataFrameDict1 = {elem: pd.DataFrame() for elem in unique_timestamp}

    for key in DataFrameDict1.keys():
        DataFrameDict1[key] = df_new[:][df_new[0] == key]

    return_list = []
    appending_string = ''

    for key in DataFrameDict1.keys():
        DataFrameDict1[key].sort_values(by=[1, 2], inplace=True)
        DataFrameDict1[key] = DataFrameDict1[key].reset_index(drop=True)
        # print(DataFrameDict1[key])
        # print("")
        appending_string += str(DataFrameDict1[key].iloc[0, 0]) + ','
        for i in range(DataFrameDict1[key].shape[0]):
            appending_string += str(DataFrameDict1[key].iloc[i, 1]) + ',' + str(DataFrameDict1[key].iloc[i, 5]) + ',' + str(DataFrameDict1[key].iloc[i, 6])
            if i != DataFrameDict1[key].shape[0]-1:
                appending_string += ','
        return_list.append(appending_string)
        appending_string = ''

    return return_list

    # raise Exception




