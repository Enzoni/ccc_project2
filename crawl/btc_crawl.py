# -*- coding: utf-8 -*-
import argparse
from textblob import TextBlob
from TwitterAPI import TwitterAPI
import nltk
import time
import couchdb
from couchdb import design, ResourceConflict
import load_file

nltk.download('punkt')


def get_tweet(item, city):
    def calculate_sentiment(text):
        blob = TextBlob(text)
        return sum([sentence.sentiment.polarity for sentence in blob.sentences])

    try:
        dic = {
            '_id': str(item['id']),
            'created_at': item['created_at'],
            'text': item['text'],
            'place_name': city,
            'sentiment': calculate_sentiment(item['text'])
        }
    except:
        dic = {}
    return dic


class TweetDB():
    def __init__(self, db_name, user_name='admin', password='123456'):
        self.url = 'http://{}:{}@172.26.133.1:5984/'.format(user_name, password)
        self.server = couchdb.Server(self.url)
        # self.server = couchdb.Server()
        # if DB doesn't exist, initialize a DB, else

        try:
            self.db = self.server.create(db_name)
            self._create_views()
        except couchdb.http.PreconditionFailed:

            self.db = self.server[db_name]

    def add_tweet(self, tweets):
        """
        add one tweets data into data base
        :param tweets: dictionary where key is column name, value is value
        """
        try:
            self.db.save(tweets)
        except ResourceConflict:
            doc = self.db.get(tweets['_id'])
            for _key, _value in tweets.items():
                doc[_key] = _value
                self.db.save(doc)

    # TODO 这里是抄的没改
    def _create_views(self):
        """ create 2 default views for the database """
        # view 1: return total count of tweets
        count_map = "function(doc) { emit(doc.id,1); }"
        count_reduce = "function(keys, values) { return sum(values); }"
        view = design.ViewDefinition("twitter",  # design document
                                     "count_tweets",  # view name
                                     count_map,  # map
                                     reduce_fun=count_reduce)

        view.sync(self.db)

        # view 2: return all stored tweet documents
        get_tweets = "function(doc) { emit(('0000000000000000000' + doc.id).slice(-19), doc); }"
        view = design.ViewDefinition("twitter", "get_tweets", get_tweets)
        view.sync(self.db)

        # view 5: return twitter_id
        get_twitter_id = "function(doc) { emit(doc.id,1); }"
        view = design.ViewDefinition("twitter", "get_twitter_id", get_twitter_id)
        view.sync(self.db)

        # view 3: return all stored tweet documents
        my_func_1 = "function(doc) { emit(doc.id,{'coordinates':doc.coordinates,'text':doc.text}); }"
        view = design.ViewDefinition("twitter", "my_f_o", my_func_1)
        view.sync(self.db)

        # view 4: return all stored tweet documents
        my_func_2 = "function(doc) { emit(doc.id,{'sentiment':doc.sentiment}); }"
        # count_reduce = "function(keys, values) { return sum(values); }"
        view = design.ViewDefinition("twitter", "my_f_t", my_func_2, reduce_fun='_sum')
        view.sync(self.db)


def main(args):
    # read TwitterAPI token
    account = load_file.account(args.account)
    bounding_box = load_file.bounding(args.bounding)[args.city]

    api = TwitterAPI(account['consumer_key'], account['consumer_secret'], account['access_token_key'],
                     account['access_token_secret'])

    # initialize DB

    db = TweetDB(args.database)

    timeout = time.time() + 10
    # send request
    r = api.request('statuses/filter', {'track': 'dogecoin',
                                        'lang': 'en',
                                        'locations': bounding_box})
    for item in r:
        time.sleep(0.5)
        # only save when coordinates is not empty
        curr_tweet = get_tweet(item, args.city)
        if curr_tweet != {}:
            db.add_tweet(curr_tweet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city", help="city name in Australia (see all city in bounding_box.json)")
    parser.add_argument("-a", "--account", help="TwitterAPI token number")
    parser.add_argument("-b", "--bounding", help="bounding box for cities", default='city_bounding.csv')
    parser.add_argument("-d", "--database", help="name of database", default='test')
    args = parser.parse_args()
    while True:
        try:
            main(args)
        except Exception as e:
            print(e)
            time.sleep(10)
            main(args)
