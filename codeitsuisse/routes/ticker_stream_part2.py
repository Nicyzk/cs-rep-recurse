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

@app.route('/tickerStreamPart2', methods=['POST'])
def tickerStreamPart2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    inputValue2 = data.get("quantityBlock")

    result = to_cumulative_delayed(inputValue,inputValue2)
    # logging.info("My result :{}".format(result))
    logging.info("output:{}".format(result))
    return json.dumps(result)

def to_cumulative_delayed(stream: list, quantity_block: int):
    list_clean = []
    for i in stream:
        list_clean.append(list(i.split(",")))

    df = pd.DataFrame.from_records(list_clean)

    UniqueTicker = df[1].unique()

    DataFrameDict = {elem: pd.DataFrame() for elem in UniqueTicker}

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df[1] == key]
        DataFrameDict[key] = DataFrameDict[key].reset_index(drop=True)

    list_of_repeat_lists = []

    for key in DataFrameDict.keys():
        DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
        duplicate_indexes = list(np.where(DataFrameDict[key][2] > 1)[0])

        for i in duplicate_indexes:
            repeat = DataFrameDict[key].loc[i]
            repeat_value = repeat.iloc[2]

            repeat[2] = 1
            repeat_list = repeat.values.tolist()
            for j in range(repeat_value):
                list_of_repeat_lists.append(repeat_list)
        append_df = pd.DataFrame.from_records(list_of_repeat_lists)

        for i in duplicate_indexes:
            DataFrameDict[key] = DataFrameDict[key].drop([i])

        DataFrameDict[key] = pd.concat([DataFrameDict[key], append_df])
        DataFrameDict[key].sort_values(by=[0], inplace=True)
        DataFrameDict[key] = DataFrameDict[key].reset_index(drop=True)

        list_of_repeat_lists.clear()

    return_list = []

    for key in DataFrameDict.keys():
        DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
        DataFrameDict[key][3] = DataFrameDict[key][3].astype(float)
        DataFrameDict[key]['notional'] = DataFrameDict[key][2] * DataFrameDict[key][3]
        DataFrameDict[key]['cum_qty'] = DataFrameDict[key][2].cumsum()
        DataFrameDict[key]['cum_not'] = DataFrameDict[key]['notional'].cumsum()

        for i in DataFrameDict[key].index:
            if (i+1) % quantity_block == 0:
                return_list.append(DataFrameDict[key].loc[i].tolist())

    return_df = pd.DataFrame.from_records(return_list)
    return_df.sort_values(by=[0], inplace=True)

    appending_string = ''
    function_return = []
    return_list_of_lists = []

    for i in range(return_df.shape[0]):
        appending_string += str(return_df.iloc[i, 0]) + ',' + str(return_df.iloc[i, 1]) + ',' + str(return_df.iloc[i, 5]) + ',' + str(return_df.iloc[i, 6])
        function_return.append(appending_string)
        return_list_of_lists.append(function_return.copy())
        appending_string = ''
        return_list.clear()
    return function_return