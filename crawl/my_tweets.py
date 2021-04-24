from TwitterAPI import TwitterAPI, TwitterPager
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import couchdb
from couchdb import design

analyzer = SentimentIntensityAnalyzer()


def load_account(file_name):
    dic = {}
    f = open('account/1.csv', mode='r')
    for i in f:
        key, value = i.strip().split(',')
        dic[key] = value
    return dic


def get_tweet(item):
    def calculate_sentiment(text):
        sentiment_dic = SentimentIntensityAnalyzer().polarity_scores(text)
        sentiment_dic.pop('compound')
        return sorted(sentiment_dic.items(), key=lambda i: i[1])[0][0]

    dic = {
        'id': item['id'],
        'id_str': item['id_str'],
        'text': item['text'],
        'coordinates': item['coordinates'],

        # TODO 预处理
        'sentiment': calculate_sentiment(item['text'])
    }
    return dic

    # try:
    #     dic = {
    #         'id': item['id'],
    #         'id_str': item['id_str'],
    #         'text': item['text'],
    #         'coordinates': item['coordinates'],
    #         'sentiment': calculate_sentiment(item['text'])
    #     }
    #     return dic
    # except:
    #     print('Element missing.')
    #     return None


class TweetDB():
    def __init__(self, dbname, url='http://localhost:5984/'):
        """
        initialize tweet

        :param dbname:
        :param url:
        """
        self.server = couchdb.Server()
        try:
            self.db = self.server.create(dbname)
            self._create_views()
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]

        except ConnectionRefusedError:
            print('Server connect failed.')
            raise ConnectionRefusedError

    def add(self, tweets):
        """
        add one tweets data into data base
        :param tweets: dictionary where key is column name, value is value
        """
        self.db.save(tweets)


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


        # view 3: return all stored tweet documents
        my_func_1 = "function(doc) { emit(doc.id,{'coordinates':doc.coordinates,'text':doc.text}); }"
        view = design.ViewDefinition("twitter", "my_f_o", my_func_1)
        view.sync(self.db)

        # view 4: return all stored tweet documents
        my_func_2 = "function(doc) { emit(doc.id,{'sentiment':doc.sentiment}); }"
        # count_reduce = "function(keys, values) { return sum(values); }"
        view = design.ViewDefinition("twitter", "my_f_t", my_func_2, reduce_fun='_sum')
        view.sync(self.db)


    # TODO 这里是抄的没改
    def count_tweets(self):
        for doc in self.db.view('twitter/count_tweets'):
            return doc.value

    # TODO 这里是抄的没改
    def get_tweets(self):
        return self.db.view('twitter/get_tweets')


if __name__ == '__main__':
    # read TwitterAPI token
    account = load_account('1.csv')
    api = TwitterAPI(account['consumer_key'], account['consumer_secret'], account['access_token_key'],
                     account['access_token_secret'])

    # initialize DB
    db = TweetDB('twitter')

    # send request
    r = api.request('search/tweets', {'q': '%23bitcon', "lang": "en",
                                      'count': 100})

    for i in range(1):
        for item in r:
            curr_tweet = get_tweet(item)

            # only save when coordinates is not empty
            if curr_tweet['coordinates'] is not None:
                db.add(get_tweet(item))
            else:
                # print('coordinates empty')
                db.add(get_tweet(item))



    # TODO 随机生成
    # dic1 = {
    #     'id': '102',
    #     'id_str': '12345678',
    #     'text': 'e china',
    #     'coordinates': [1, 2],
    #
    #     # TODO 预处理
    #     'sentiment': 'pos'
    # }
    #
    # dic2 = {
    #     'id': '103',
    #     'id_str': '123456789',
    #     'text': 'ausna',
    #     'coordinates': [2, 3],
    #
    #     # TODO 预处理
    #     'sentiment': 'neg'
    # }
    # db.add(dic1)
    # db.add(dic2)