
import json
from flask import Flask, request, render_template
import sqlite3


app = Flask(__name__)
conn = sqlite3.connect('ora')
cursor = conn.cursor()



@app.route("/", methods=["GET", "POST"])
def hello():
    sql = ""
    if request.method == "POST":
        data = request.json
        print data
        try:
            sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % (
            data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], int(data['Time']))
            ret = cursor.execute(sql)
        except :
            pass
        return "OK"
    else:
        return render_template("index.html")


@app.route("/data", methods=["GET"])
def getdata():
    cursor.execute("SELECT `time`,`mem_usage` FROM `stat`")
    ones = [[i[0] * 1000, i[1]] for i in cursor.fetchall()]
    return "%s(%s);" % (request.args.get('callback'), json.dumps(ones))


if __name__ == "__main__":
    app.run(host="192.168.0.107", port=8888, debug=True)