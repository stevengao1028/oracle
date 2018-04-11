# !/usr/bin/python
# -*- coding: UTF-8 -*-
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
        print data['name']
        print data['time']
        print data['cpu']
        print data['disk']
        print data['mem']
        print data['uptime']
        print data['net']
        print data['load']
        sql_value = '\''+data['name']+'\''+',\''+data['time']+'\''
        # ,data['time'],data['mem']['MemFree'],data['mem']['MemUsed'],data['mem']['MemTotal']\
        #             ,data['uptime']['day'],data['uptime']['hour'],data['uptime']['minute'],data['uptime']['Free rate']\
        #             ,data['cpu']['lcount'],data['cpu']['rate'],data['cpu']['pcount'],data['cpu']['pcount'] \
        #             ,data['disk']['used'],data['disk']['total'],data['disk']['percent'],data['disk']['name'],'+data['disk']['free']\
        #             +','+data['net'][0]['interface']+','+data['net'][0]['ReceiveBytes']+','+data['net'][0]['TransmitBytes'] \
        #             +','+data['net'][1]['interface'] + ',' + data['net'][1]['ReceiveBytes'] + ',' + data['net'][1]['TransmitBytes'] \
        #             +','+data['load']['lavg_1']+','+data['load']['lavg_5']+','+data['load']['lavg_15']+','+data['load']['last_pid']
        print sql_value
        sql = "INSERT INTO stat VALUES " + sql_value
        #     'MemTotal'] + ',' + data['LoadAvg'] + ',' + str(data['Time'])
        # print sql
        # try:
        #     ret = cursor.execute(sql)
        #     print ret
        # except :
        #     pass
        return "OK"
    else:
        return render_template("index.html")


@app.route("/data", methods=["GET"])
def getdata():
    cursor.execute("SELECT `time`,`mem_usage` FROM `stat`")
    ones = [[i[0] * 1000, i[1]] for i in cursor.fetchall()]
    return "%s(%s);" % (request.args.get('callback'), json.dumps(ones))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)