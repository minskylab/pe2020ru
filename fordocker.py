from flask import Flask, escape, request, jsonify
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

stopFlag = threading.Event()
loop = asyncio.new_event_loop()


sw = worker.GovernmentWorker(
    stopFlag, loop, workspace="/data", search=search, since=since, interval_s=interval)


@app.route('/freqs')
def freqs():
    result = {"data": [{"text": freq[1], "value": freq[0]}
                       for freq in sw.freqs]}
    return jsonify(result)


sw.start()

app.run(host="0.0.0.0", port=port)
