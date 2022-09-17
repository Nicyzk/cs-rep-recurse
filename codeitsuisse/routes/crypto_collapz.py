import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/crypto_collapzz', methods=['POST'])
def crpyto_collapzz():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("stream")
    result = crpyto_collapzz(inputValue)
    logging.info("output:{}".format(result))
    return json.dumps(result)


def crpyto_collapz(stream: list):

    list_of_lists = []

    for i in range(len(stream)):

        testcase_return = []

        for j in range(len(stream[i])):
            list_of_values = [stream[i][j]]
            number = stream[i][j]


            if number == 1 or number == 2:
                list_of_values.append(4)

            while number != 1:
                if number % 2 == 0:
                    # print(number // 2)
                    list_of_values.append(number // 2)
                    number = number // 2
                    continue

                elif number % 2 == 1:
                    number = 3 * number + 1
                    # print(result)
                    list_of_values.append(number)
                    continue

            testcase_return.append(max(list_of_values))

        list_of_values.clear()

        list_of_lists.append(testcase_return)
    return list_of_lists




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
