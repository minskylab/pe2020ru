from flask import Flask, escape, request, jsonify
from flask_cors import CORS, cross_origin

import worker
import threading
import asyncio

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

stopFlag = threading.Event()
loop = asyncio.new_event_loop()

sw = worker.GovernmentWorker(stopFlag, loop)


@app.route('/freqs')
@cross_origin()
def freqs():
    data = [{"text": freq[1], "value": freq[0]} for freq in sw.freqs]
    result = {}
    result["data"] = data
    result["last_update"] = sw.last_update()
    return jsonify(result)


sw.start()
app.run(host="0.0.0.0", port=8080)
