import couchdb
import json
import re
from setting import host, port, username, password, db_name1, db_name2
# import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

def link_db(host, port, username, password):
    server = couchdb.Server('http://' + username + ':' + password + '@' + host + ':' + port)
    return server


server = link_db(host, port, username, password)
dd = server[db_name1]
aurin = server[db_name2]


app=Flask(__name__)
CORS(app, resources=r'/*')
def get_sen(city, date):
    id = None
    if city == 'Adelaide':
        id = 'btc_a_0505'
    if city == 'Brisbane':
        id = 'btc_b_0505'
    if city == 'g':
        id = 'btc_g_0505'
    if city == 'Melbourne':
        id = 'btc_m_0505'
    if city == 'Perth':
        id = 'btc_p_0505'
    if city == 'Sydney':
        id = 'btc_s_0505'

    info = dd.get(id=id)
    if date == None:
        return json.dumps(info["overall"])
    else:

        dic = {}
        for i in info:
            if re.search(date, i):
                da = date + '-'
                hour = re.sub(da, '', i)
                dic[hour] = info[i]
        total_sen = 0
        total_count = 0
        total_po = 0
        total_ne = 0
        for i in dic:
            total_sen += dic[i]['sum']
            total_count += dic[i]['count']
            total_po += dic[i]['positive']
            total_ne += dic[i]['negative']
        dic['total'] = {"sum": total_sen, "count": total_count, "positive": total_po, "negetive": total_ne}

    return dic


def a_ur(city):
    edu = 'highest_year_completed'
    emp = 'education_employment'
    fam = 'famliy'
    geo = 'geomatry'
    income = 'personal_income'
    job = 'num_job'
    if city == 'Sydney':
        code = '1GSYD'
    if city == 'Melbourne':
        code = "2GMEL"
    if city == 'Brisbane':
        code = "3GBRI"
    if city == 'Adelaide':
        code = "4GADE"
    if city == 'Perth':
        code = "5GPER"
    if city == 'Hobart':
        code = "6GHOB"
    if city == 'Darwin':
        code = "7GDAR"
    if city == 'Australian Capital Territory':
        code = "8ACTE"
    edu_ = aurin.get(id=edu)
    emp_ = aurin.get(id=emp)
    fam_ = aurin.get(id=fam)
    geo_ = aurin.get(id=geo)
    income_ = aurin.get(id=income)
    job_ = aurin.get(id=job)
    aur = {}
    for i in edu_["features"]:

        if i["properties"]["gccsa_code_2016"] == code:
            aur["edu"] = i["properties"]["f_hghst_yr_schl_ns_tot"]
            break
    for i in income_["features"]:
        if i["properties"]["gccsa_code_2016"] == code:
            aur["income"] = i["properties"]["mean_aud_2014_15"]
            break
    for i in emp_["features"]:

        if i["properties"]["gccsa_code_2016"] == code:
            aur["unemp"] = i["properties"]["labour_force_status_persons_aged_15_years_census_unemployed_num"]
            break
    for i in emp_["features"]:
        if i["properties"]["gccsa_code_2016"] == code:
            aur["emp"] = i["properties"]["labour_force_status_persons_aged_15_years_census_employed_num"]
            break
    return aur


@app.route("/aurin", methods=["GET"])
def get_au(city, date):
    dic = get_sen(city, date)
    aur = a_ur(city)
    final_dic = {}
    final_dic["sentiment"] = dic['total']['sum']
    final_dic["count"] = dic['total']['count']
    final_dic["positive"] = dic['total']['positive']
    final_dic["negetive"] = dic['total']['negetive']
    final_dic['edu'] = aur["edu"]
    final_dic['income'] = aur["income"]
    final_dic['emp'] = aur["emp"]
    final_dic['unemp'] = aur["unemp"]
    return json.dumps(final_dic)


@app.route("/dogcoin", methods=["GET"])
def get_dc(city, date):
    final_dic = {}
    dic = get_sen(city, date)
    dic.pop("total")
    final_dic['sen_hourly'] = {}
    for i in dic:
        final_dic['sen_hourly'][i] = dic[i]["sum"]
    final_dic['dogcoin_price_hourly'] = {"0": 0.468447,
                                         "1": 0.468014,
                                         "2": 0.454778,
                                         "3": 0.471,
                                         "4": 0.474527,
                                         "5": 0.472173,
                                         "6": 0.464399,
                                         "7": 0.407149,
                                         "8": 0.425932,
                                         "9": 0.450045,
                                         "10": 0.454539,
                                         "11": 0.456378,
                                         "12": 0.453824,
                                         "13": 0.447803,
                                         "14": 0.448042,
                                         "15": 0.432809}
    return json.dumps(final_dic)


@app.route("/bar", methods=["GET"])
def get_bar(date):
    city_ = {}
    for name in ['Sydney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth']:
        aur = a_ur(name)
        sen = get_sen(name, date)
        city_[name] = {}
        city_[name]['ave_sen'] = (sen['total']["sum"]) / (sen["total"]["count"])
        city_[name]['edu'] = aur["edu"]
        city_[name]['income'] = aur["income"]
        city_[name]['emp'] = aur["emp"]
        city_[name]['unemp'] = aur["unemp"]
    return json.dumps(city_)
