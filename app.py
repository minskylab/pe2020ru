from flask import Flask, escape, request, jsonify, send_file
from flask_cors import CORS, cross_origin

from humanfriendly import format_timespan
import worker
import threading
import asyncio
import about

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

stopFlag = threading.Event()
loop = asyncio.new_event_loop()


config = {
    "query_search": "Elecciones2020",
    "since_date": "2019-10-01",
    "time_interval": format_timespan(1800)
}

gw = worker.GovernmentWorker(stopFlag, loop)


@app.route('/freqs')
@cross_origin()
def freqs():
    data = [{"text": freq[1], "value": freq[0]} for freq in gw.freqs]
    result = {}
    result["data"] = data
    result["last_update"] = gw.last_update()
    return jsonify(result)


@app.route('/about')
@cross_origin()
def about_us():
    return "Hello"


@app.route('/about/json')
@cross_origin()
def about_us_json():
    result = {}
    result["description"] = about.description
    result["about"] = about.about
    result["config"] = config
    result["endpoints"] = about.endpoints
    result["endpoints"]["dataframes"] = [
        f"/dataframe/{df}" for df in gw.available_dataframes()]
    return jsonify(result)


@app.route('/dataframe/<name>')
@cross_origin()
def dataframe(name):
    if not name in gw.available_dataframes():
        return jsonify({"error": "invalid or not exist dataframe name"})

    return send_file(gw.path_of_dataframe(name))


gw.start()
app.run(host="0.0.0.0", port=8080)
