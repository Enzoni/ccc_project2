import couchdb
import pandas as pd
from couchdb import ResourceConflict


"""
used to test function 

"""


if __name__ == '__main__':
    couch = couchdb.Server()
    try:
        db = couch.create('test')
    except:
        db = couch['test']

    doc1 = {'_id': '123', 'foo': 'bar'}
    doc2 = {'_id': '123', 'foo': 'yeah'}
    doc4 = {'_id': '123', 'foo': '222'}
    doc3 = {'_id': '111', '1': '2'}

    for tweets in [doc1, doc2, doc3, doc4]:
        # db.save(i)
        # print()
        try:
            db.save(tweets)
        except ResourceConflict:
            doc = db.get(tweets['_id'])
            for _key, _value in tweets.items():
                doc[_key] = _value
                db.save(doc)
