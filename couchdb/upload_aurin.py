# COMP90024 Assignment 2
# Team: 38
# City: Melbourne
# Members:
# Ziran Gu (1038782)
# Jueying Wang (1016724)
# Yifei Zhou(980429)
# Jiakai Ni (988303)
# Ziyue Liu (1036109)


import couchdb
import os
import json

db_auth = {
    "ip": "172.26.132.206", 
    "port": "5984", 
    "user": "admin", 
    "pwd": "password"
}
def main():

    # db url
    url = "http://" + db_auth["user"] + ":" + db_auth["pwd"] \
                    + "@" + db_auth["ip"] + ":" + db_auth["port"] + "/"

    # connect to coudb server
    server = couchdb.Server(url=url)

    # create a new db to store aurin data
    try:
        aurin_db = server.create('aurin')
    except couchdb.http.PreconditionFailed:
        # existing db
        aurin_db = server['aurin']

    # each aurin file
    for filename in os.listdir('aurin'):

        # read content
        with open(os.path.join('aurin', filename)) as f:
            data = json.load(f)

        # set document name
        document_id = filename.rstrip(".json")
        data['_id'] =document_id

        if document_id in aurin_db:
            # to update existing doc
            data['_rev'] = aurin_db.get(document_id)['_rev']

        print(data.keys())

        aurin_db.save(data)



        
        

if __name__ == "__main__":
    main()
