import couchdb
from setting import host, port, username, password, db_name
#import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

def link_db(host, port, username, password):
    server = couchdb.Server('http://' + username + ':' + password + '@' + host + ':' + port)
    return server


server = link_db(host, port, username, password)
dd = server[db_name]


app=Flask(__name__)
CORS(app, resources=r'/*')

@app.route("/nb",methods=["GET"])
def get_sen(database, city, date):
    id = None
    if city == 'a':
        id = 'btc_a_0505'
    if city == 'b':
        id = 'btc_b_0505'
    if city == 'g':
        id = 'btc_g_0505'
    if city == 'm':
        id = 'btc_m_0505'
    if city == 'p':
        id = 'btc_p_0505'
    if city == 's':
        id = 'btc_s_0505'
    #if id == None:
    if date == None:
        return dd.get(id=id)["overall"]
    else:
        return dd.get(id=id)[date]

