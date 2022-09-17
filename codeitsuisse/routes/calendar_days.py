import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/calendar_days', methods=['POST'])
def calendar_days():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("numbers")
    result = calendar_day(inputValue)
    logging.info("output:{}".format(result))
    return json.dumps(result)

def calendar_day(stream: list):
    
