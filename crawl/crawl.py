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
    def __init__(self, db_name, user_name='admin', password='password'):
        self.url = 'http://{}:{}@172.26.132.206:5984/'.format(user_name, password)
        self.server = couchdb.Server(self.url)
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

    def _create_views(self):
    	return


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

