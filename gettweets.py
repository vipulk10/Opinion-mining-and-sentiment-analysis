import argparse
import urllib
import json
import os
import oauth2
from pre import processAll
class TwitterData:
    def parse_config(self):#this method is used to get the api keys from the user having a twitter account through which we can acesss twitter 
        config = {}
        # from file args
        if os.path.exists('config.json'):
            with open('config.json') as f:
                config.update(json.load(f))
        else:
            # may be from command line
            parser = argparse.ArgumentParser()

            parser.add_argument('-ck', '--consumer_key', default=None, help='Your developper `Consumer Key`')
            parser.add_argument('-cs', '--consumer_secret', default=None, help='Your developper `Consumer Secret`')
            parser.add_argument('-at', '--access_token', default=None, help='A client `Access Token`')
            parser.add_argument('-ats', '--access_token_secret', default=None, help='A client `Access Token Secret`')

            args_ = parser.parse_args()
            def val(key):
                return config.get(key)\
                    or getattr(args_, key)\
                    or raw_input('Your developper `%s`: ' % key)
            config.update({
                'consumer_key': val('consumer_key'),
                'consumer_secret': val('consumer_secret'),
                'access_token': val('access_token'),
                'access_token_secret': val('access_token_secret'),
            })
        # should have something now
        return config
    #end
# following code taken from https://twittercommunity.com/t/python-oauth2-example-code-needs-update/50873
    def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
        config = self.parse_config()
        consumer = oauth2.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
        token = oauth2.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
        client = oauth2.Client(consumer, token)

        resp, content = client.request(
            url,
            method=http_method,
            body=post_body or '',
            headers=http_headers
        )
        return content
    #end

    #start getTwitterData
    #https://dev.twitter.com/rest/reference/get/search/tweets
    def getData(self, keyword, params = {}):
        maxTweets = 25
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        data = {'q': keyword, 'lang': 'en', 'result_type': 'mixed', 'count': maxTweets, 'include_entities': 0}

        #Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value

        url += urllib.urlencode(data)

        response = self.oauth_req(url)
        jsonData = json.loads(response)
        tweets = []
        if 'errors' in jsonData:
            print "API Error"
            print jsonData['errors']
        else:
            for item in jsonData['statuses']:
                tweets.append(item['text'])
        tweets = list(set(tweets))
        #for i in tweets:
            #i=processAll(i)
        return tweets
    #end
'''
td = TwitterData()
t=td.getData('tobacco')
for i in t:
    print i.encode('utf-8')
'''