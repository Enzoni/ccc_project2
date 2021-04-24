


database = 'twitterutils'

# -*- coding:utf-8 -*-
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterPager


def search_tweets(the_consumer_key, the_consumer_secret, the_access_token_key,
                  the_access_token_secret, the_proxy_url):
    """
    搜索含有特定“内容”的推文
    :param the_consumer_key: 已有的consumer_key
    :param the_consumer_secret: 已有的consumer_secret
    :param the_access_token_key: 已有的access_token_key
    :param the_access_token_secret: 已有的access_token_secret
    :param the_proxy_url: 代理及端口号
    :return:
    """
    api = TwitterAPI(consumer_key=the_consumer_key,
                     consumer_secret=the_consumer_secret,
                     access_token_key=the_access_token_key,
                     access_token_secret=the_access_token_secret,
                     proxy_url=the_proxy_url)
    r = TwitterPager(api, 'search/tweets', {'q': 'pizza', 'count': 10})
    for item in r.get_iterator():
        if 'text' in item:
            print(item['text'])
        elif 'message' in item and item['code'] == 88:
            print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
            break


if __name__ == "__main__":
    consumerKey = "XLosXwDjbJagoBKQIFXpz9NVl"  # 分别对应填写你申请的四项内容
    consumerSecret = "YoBpv8HTCIdApNM3po5tfKgqXWFGJeOMoNQHbUEKAt2N287Rln"
    accessToken = "1106763616055750656-VKG9o9WrpKLzC1Zd6OyvDSDbQmQKJX"
    accessTokenSecret = "Kc7LTIFwMz4rtfBJKHGCIQqIkmVzFATpzgF4Kb9PENyyr"


    search_tweets(the_consumer_key=consumerKey,
                  the_consumer_secret=consumerSecret,
                  the_access_token_key=accessToken,
                  the_access_token_secret=accessTokenSecret,
)
