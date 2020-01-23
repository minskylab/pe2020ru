from flask import Flask, escape, request, jsonify
from flask_cors import CORS, cross_origin

import worker
import threading
import asyncio
import os

port = os.environ.get("PORT", "8080")
search = os.environ.get("SEARCH_QUERY", "Elecciones2020")
since = os.environ.get("SINCE_DATE", "2019-10-01")
interval = os.environ.get("INTERVAL_TIME", 1800)
interval = int(interval)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

stopFlag = threading.Event()
loop = asyncio.new_event_loop()


sw = worker.GovernmentWorker(
    stopFlag, loop, workspace="/data", search=search, since=since, interval_s=interval)


@app.route('/freqs')
@cross_origin()
def freqs():
    data = [{"text": freq[1], "value": freq[0]} for freq in sw.freqs]
    result = {}
    result["data"] = data
    result["last_update"] = sw.last_update()
    return jsonify(result)


sw.start()

app.run(host="0.0.0.0", port=port)
