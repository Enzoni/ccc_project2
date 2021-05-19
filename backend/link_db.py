import couchdb
import json
import re
from setting import host, port, username, password, db_name1, db_name2, db_name3
# import csv
from flask import Flask, request, jsonify
from flask_cors import CORS


def link_db(host, port, username, password):
    server = couchdb.Server('http://' + username + ':' + password + '@' + host + ':' + port)
    return server


server = link_db(host, port, username, password)
dd = server[db_name1]
aurin = server[db_name2]
dogcoin = server[db_name3]


app = Flask(__name__)
CORS(app, resources=r'/*')
def get_dogcoin(date):
    do = dogcoin.get(id = 'dog')
    for key in do:
        if key == date:
            price_list = do[key]
    dic = {}
    for i in range(len(price_list)):
        dic[str(i+1)] = price_list[i]
    return dic

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
    if date is None:
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
        dic['total'] = {"sum": total_sen, "count": total_count, "positive": total_po, "negative": total_ne}

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

        if i["properties"]["gcc_code16"] == code:
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


@app.route("/api/get_data_statistic", methods=["POST"])
def get_au():
    try:
        input = request.json
        dic = get_sen(input['city'], input['date'])
        aur = a_ur(input['city'])
        final_dic = {}
        final_dic["sentiment"] = dic['total']['sum']
        final_dic["count"] = dic['total']['count']
        final_dic["positive"] = dic['total']['positive']
        final_dic["negative"] = dic['total']['negative']
        final_dic['edu'] = aur["edu"]
        final_dic['income'] = aur["income"]
        final_dic['emp'] = aur["emp"]
        final_dic['unemp'] = aur["unemp"]
        response = jsonify(isError=False, message="Success", statusCode=200, data=final_dic)
        return response
    except Exception as e:
        return jsonify(isError=True, message="{}".format(e), statusCode=404)


@app.route("/api/get_dogcoin_price", methods=["POST"])
def get_dc():
    try:
        input = request.json
        final_dic = {}
        dic = get_sen(input['city'], input['date'])

        # dic.pop("total")

        #del dic['total']
        final_dic['sen_hourly'] = {}
        for i in dic:
            if i == 'total':
                continue
            final_dic['sen_hourly'][i] = dic[i]["sum"]
        final_dic['dogcoin_price_hourly'] = get_dogcoin(input['date'])
        #print(final_dic)
        response = jsonify(isError=False, message="Success", statusCode=200, data=final_dic)
        return response
    except Exception as e:
        return jsonify(isError=True, message="{}".format(e), statusCode=404)


@app.route("/api/get_cities", methods=["POST"])
def get_city():
    try:
        result = {
            'cities': [
                {
                    'city_name': 'Melbourne',
                    'position': [-37.8136, 144.9631]
                },
                {
                    'city_name': 'Sydney',
                    'position': [-33.8688, 151.2093]
                },
                {
                    'city_name': 'Brisbane',
                    'position': [-27.4705, 153.0260]
                },
                {
                    'city_name': 'Perth',
                    'position': [-31.9523, 115.8613]
                },
                {
                    'city_name': 'Adelaide',
                    'position': [-34.9285, 138.6007]
                }
            ]
        }
        response = jsonify(isError=False, message="Success", statusCode=200, data=result)
        return response
    except Exception as e:
        return jsonify(isError=True, message="{}".format(e), statusCode=404)
    pass


@app.route("/api/bar", methods=["POST"])
def get_bar():
    input = request.json
    date = input['date']
    city_ = {}
    city_['ave_sen'] = {}
    city_['edu'] = {}
    city_['income'] = {}
    city_['emp'] = {}
    city_['unemp'] = {}
    try:
        for name in ['Sydney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth']:
            aur = a_ur(name)
            sen = get_sen(name, date)

            city_['ave_sen'][name] = (sen['total']["sum"]) / (sen["total"]["count"])
            city_['edu'][name] = aur["edu"]
            city_['income'][name] = aur["income"]
            city_['emp'][name] = aur["emp"]
            city_['unemp'][name] = aur["unemp"]
        response = jsonify(isError=False, message="Success", statusCode=200, data=city_)
        return response
    except Exception as e:
        return jsonify(isError=True, message="{}".format(e), statusCode=404)


# @app.route('/', methods=['GET'])
# def hello_world():
#     return 'Ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
