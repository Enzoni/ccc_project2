import couchdb

# class TweetStore(object):


if __name__ == '__main__':
    couch = couchdb.Server()
    db = couch['test']

    map_fun = '''
    function(doc) {
        emit([doc._id], doc.foo);
    }'''
    results = db.query(map_fun)

    for i in results:
        print(i)
    # db = couch['test']
    # doc = {'foo': 'bar'}
    # db.save(doc)
    # print(db)

    def _create_views(db):
        count_map = 'function(doc) { emit(doc.id, 1); }'
        view = couchdb.design.ViewDefinition('twitter', 'count_tweets', count_map, reduce_fun=count_reduce)
        view.sync(db)