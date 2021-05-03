import couchdb

if __name__ == '__main__':
    couch = couchdb.Server()
    db = couch.create('test')  # newly created

    doc = {'foo': 'bar'}
    db.save(doc)