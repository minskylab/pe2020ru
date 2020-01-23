from flask import Flask, escape, request, jsonify
import worker
import threading

app = Flask(__name__)


stopFlag = threading.Event()
sw = worker.GovernmentWorker(stopFlag)


@app.route('/freqs')
def freqs():
    result = {"data": [{"text": freq[1], "value": freq[0]}
                       for freq in sw.freqs]}
    return jsonify(result)


sw.start()
app.run(host="0.0.0.0", port=8080)
