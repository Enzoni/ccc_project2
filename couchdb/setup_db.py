import couchdb
from couchdb import design
from datetime import datetime
import time

db_auth = {
    "ip": "172.26.132.206", 
    # "ip": "172.26.133.1",
    "port": "5984", 
    "user": "admin", 
    "pwd": "password"
    # "pwd": "123456"
}


def create_views(db):
    """ 2 views for getting info about sentiment """
    # view 1: return sum and counts of sentiment for each hour
    map = '''function (doc) {
                var date = new Date(Date.parse(doc.created_at))
                var newDate = date.getFullYear() + "-" + (date.getMonth() + 1) 
                                + "-" + date.getDate() + "-" + date.getHours()
                emit(newDate, doc.sentiment);
            }'''

    reduce = '''function(keys, values, rereduce) {
                    if (rereduce) {
                        return {
                            'sum': values.reduce(function(a, b) { return a + b.sum }, 0),
                            'count': values.reduce(function(a, b) { return a + b.count }, 0),
                            'positive': values.reduce(function(a, b) { return a + b.positive }, 0),
                            'negative': values.reduce(function(a, b) { return a + b.negative }, 0)
                        }
                    } else {

                      var pos = 0;
                      var neg = 0;
                      values.forEach(function (value) {
                        if (value > 0) {
                          pos += 1;
                        } else if (value < 0) {
                          neg += 1;
                        }
                      });

                        return {
                            'sum': sum(values),
                            'count': values.length,
                            'positive': pos,
                            'negative': neg
                        }
                    } 
                }'''
    view = design.ViewDefinition("sentiment",       # design document
                                 "hour_sentiment",  # view name
                                 map,       # map
                                 reduce)
    view.sync(db)

    # view 2: return overall sum and counts of sentiment
    map2 = '''function(doc) { 
                emit(doc._id, doc.sentiment); 
            }'''
    reduce2 = reduce   # same as view 1: 'stats'
    view2 = design.ViewDefinition("sentiment",
                                  "sentiment",
                                  map2,
                                  reduce2)
    view2.sync(db)

def get_sentiment(db):
    return db.view("sentiment/sentiment")

def get_hour_sentiment(db):
    return db.view("sentiment/hour_sentiment", group=True)


def main():

    # db url
    url = "http://" + db_auth["user"] + ":" + db_auth["pwd"] \
                    + "@" + db_auth["ip"] + ":" + db_auth["port"] + "/"

    # connect to coudb server
    server = couchdb.Server(url=url)

    # create a new db to store analysis results
    try:
        analysis_db = server.create('analysis')
    except couchdb.http.PreconditionFailed:
        # existing db
        analysis_db = server['analysis']

    for db_name in server:
        # skip non-btc databases
        if not db_name.startswith("btc_") or db_name == "btc_n_0505":
            continue
        db = server[db_name]

        # create view for that db
        create_views(db)

    print("UPDATED VIEWS")

    # run forever
    while True:

        for db_name in server:
            # skip non-btc databases
            if not db_name.startswith("btc_") or db_name == "btc_n_0505":
                continue
            db = server[db_name]

            sentiments = get_sentiment(db)
            hours = get_hour_sentiment(db)

            hour_dict = {'_id':db_name}

            # print(db_name)

            if db_name in analysis_db:
                # to update existing doc
                hour_dict['_rev'] = analysis_db.get(db_name)['_rev']

            for item in sentiments:
                # will run for one time only
                hour_dict['overall'] = item.value

            for item in hours:
                hour_dict[item.key] = item.value

            now = datetime.now()
            print("UPDATED BY: ", now)

            hour_dict['updated_by'] = str(now)

            print(hour_dict['overall'])

            analysis_db.save(hour_dict)

        time.sleep(600)

        
        

if __name__ == "__main__":
    main()