# -*- coding: utf-8 -*-


"""
used to check duplicate


"""

import couchdb
import pandas as pd

if __name__ == '__main__':
    user_name = 'admin'
    password = '123456'
    url = 'http://{}:{}@172.26.133.1:5984/'.format(user_name, password)
    couch = couchdb.Server(url)
    db = couch['btc_s']

    rows = db.view('_all_docs', include_docs=True)

    # for i in rows:
    #     print(i['doc']['id'])
    #     break
    data = [i['doc'] for i in rows]

    df = pd.DataFrame(data)['id'].tolist()
    print(len(df))
    print(len(set(df)))