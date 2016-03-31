import tweepy

from corrections import KEYWORD_TO_TRIGGERS
import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        # don't bother if it's a retweet
        try:
            if status.retweeted_status:
                return
        except: # if it doesn't have the field, it's not a retweet
            pass
        
        for keyword in KEYWORD_TO_TRIGGERS:
            should_respond = False
            triggers = KEYWORD_TO_TRIGGERS[keyword]
            for trigger in triggers:
                if status.text.find(trigger) > -1:
                    should_respond = True
                    break

            if should_respond:
                print 'screen_name: %s; text: %s\n' % (status.user.screen_name, status.text)
                api.update_status('.@%s did you mean %s?' % (status.user.screen_name, keyword), status.id)

listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=KEYWORD_TO_TRIGGERS.keys())
