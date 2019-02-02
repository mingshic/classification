#!/usr/bin/env python

import os
import sys
from flask import Flask, jsonify, abort, request, make_response
import json
import urllib.request
#import urllib2
#import codecs
import simplejson
from alarm_run import rule_match,rule_match_from_send

from db.execute_command import command_ready
from db.data_processing import data_type 

from top_url import url

app = Flask(__name__)
#app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config['JSON_AS_ASCII'] = False

predict_file_local = "cnn_model"
alarm_file_local = "alarm_processing"



def writeFile(way,content,open_file):
    if way == "type":
        with open(open_file, "wb") as code:
            code.write(content) 
    elif way == "txt":
        with open(open_file, "w") as code:
            code.write(content)    
    elif way == None:
        with open(open_file, "w") as code:
            code.write(content)

def predict_command(open_file):
    response = list(os.popen("python predict_contract_cnn.py %s" % open_file))[0].strip()
    return response


@app.route('/api/word', methods=['GET', 'POST'])
def Contract():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data.decode('utf8'))
        try:
            if data['request_type'] != '':
                try:
                    value = data['request_type']
                    url_endswith = value.split(".")[-1]
                    f = urllib.request.urlopen(value)
                    url_file_content = f.read()
                    open_file = predict_file_local+"/predict_files" + '/' + "file"+'.'+url_endswith
                    writeFile("type", url_file_content, open_file)
                except:
                    return make_response(jsonify({"code": 0, "data": "The key's value of 'request_type' is not correct, please check your value(url)"}), 404) 
                return jsonify({"code": 1, "data": predict_command(open_file)})
        except:
            return make_response(jsonify({"code": 0, "data": "The key 'request_type' was missing, please check your 'request_type' field"}), 404)

        try:
            if data['request_data'] != '':
                value = data['request_data']
                text_content = value
                open_file = predict_file_local+"/predict_files" + '/' + "file" + '.' + 'txt'
                writeFile("txt", text_content, open_file)
                return jsonify({"code": 1,"data": predict_command(open_file)})
        except:
            return make_response(jsonify({"code": 0, "data": "The key 'request_data' was missing, please check your 'request_data' field"}), 404)
                        
    return jsonify({"code": 0,"data": "no data"})    

@app.route('/api/alarm', methods=['GET', 'POST'])
def Alarm():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data.decode('utf8'))
        try:
            if data['request_data'] != '':
                value = data['request_data']
                alarm_content = value
                open_file = alarm_file_local + '/' + "Alarm_file"
                writeFile(None, alarm_content, open_file)
                rule_policySet = rule_match(open_file)
                return jsonify({"code": 1,"data": rule_policySet})
        except:
            return make_response(jsonify({"code": 0, "data": "The key 'request_data' was missing, please check your 'request_data' field"}), 404)
    return jsonify({"code": 0,"data": "no data"})


@app.route('/api/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.data
        data = json.loads(data.decode('utf8'))
        
#        content_dict = {}
        data_content = ""
        
        try:
            if data['request_data'] != '':
                value = data['request_data']
                alarm_content = value
                alarm_content = data_type(alarm_content)

                rule_policySet = rule_match_from_send(alarm_content)
                req = urllib.request.urlopen(url+alarm_content[1]['SN'])
                top_response = json.loads(req.read().decode("utf8"))["data"]
           
                print (alarm_content)
                alarm_content.append({"top_response": top_response})
                print (alarm_content)
                insert_db = command_ready()
                insert_db.insert_alarm(alarm_content, rule_policySet)
                return jsonify({"code": 1,"data": rule_policySet})
        except:
            return make_response(jsonify({"code": 0, "data": "The key 'request_data' was missing, please check your 'request_data' field"}), 404)
    return jsonify({"code": 0,"data": "no data"})

#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
