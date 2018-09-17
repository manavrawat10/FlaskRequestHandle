# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:36:37 2018

@author: Manav
"""

from flask import Flask,jsonify,request
from datetime import datetime
import random
import time
app = Flask(__name__)

req={"GET":{"minute":0,"hour":0,"active":0,"total":0,"last":'1970-01-01 00:00:01.441985',"refresh":'1970-01-01 00:00:01.441985'},
"POST":{"minute":0,"hour":0,"active":0,"total":0,"last":'1970-01-01 00:00:01.441985',"refresh":'1970-01-01 00:00:01.441985'},
"PUT":{"minute":0,"hour":0,"active":0,"total":0,"last":'1970-01-01 00:00:01.441985',"refresh":'1970-01-01 00:00:01.441985'},
"DELETE":{"minute":0,"hour":0,"active":0,"total":0,"last":'1970-01-01 00:00:01.441985',"refresh":'1970-01-01 00:00:01.441985'}}

@app.route('/process/<extra>',methods=['GET','POST','DELETE','PUT','PATCH'])
def process(extra):
    dur=random.randint(16,30)
    # check the request method
    met=str(request.method)
    req[met]["active"]=req[met]["active"]+1
    last_time = datetime.strptime(str(req[met]["last"]), '%Y-%m-%d %H:%M:%S.%f')
    cur_time=datetime.now()
    if (cur_time-last_time).total_seconds()<=60 or req[met]["total"]==0:
        req[met]["minute"]+=1
        req[met]["hour"]+=1
    elif(cur_time-last_time).total_seconds()<=3600:
        req[met]["hour"]+=1
    else:
        req[met]["minute"]=1
        req[met]["hour"]=1
    bodypart=""
    if request.method == "POST":
        bodypart=request.data
    time.sleep(dur)
    response={"time": cur_time,
     "method":request.method,
     "headers": str(request.headers),
     "path": str(request.path),
     "query": request.args,
     "body": bodypart,
     "duration": str(dur)     }
    req[met]["active"]=0
    req[met]["total"]+=1
    req[met]["last"]=cur_time
    req[met]["refresh"]=cur_time
    
    return jsonify(response)

@app.route('/stats',methods=['GET'])
def stats():
    cur_time=datetime.now()
    for met in req:
        ref_time=datetime.strptime(str(req[met]["refresh"]), '%Y-%m-%d %H:%M:%S.%f')
        if (cur_time-ref_time).total_seconds()>=60 and (cur_time-ref_time).total_seconds()<=3600:
            req[met]["minute"]-=1
        elif(cur_time-ref_time).total_seconds()>3600 and req[met]["total"]!=0:
            req[met]["hour"]-=1
        req[met]["refresh"]=cur_time
    return jsonify(req)
if __name__ == '__main__':
    app.run()
