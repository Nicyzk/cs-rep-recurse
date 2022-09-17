import pwn

import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/payload_stack', methods=['GET'])
def payload_stack():
    # io = pwn.process('./stack')
    with open('/payload_stack', 'rb') as f:
        payload = f.read()

    # io.send(payload)
    # output = io.recv().decode('latin-1')
    return json.dumps(payload)