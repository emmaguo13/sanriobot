#fix github
#get personality insights
#get photos
#test bot
#release bot
import tweepy, nltk
from textblob import TextBlob

CONSUMER_KEY = 'I9tO6b8wMWeL8zcSiL73KM6sQ'
CONSUMER_SECRET = 'jUHEiAx7NnuIa5Vz9Hy81VrQHODus2m5yyVOd5EG6moXgUlPFo'
ACCESS_KEY = '1267989567484817410-lxX26aDMpqHM92B4SQ7dv9x3yN3sLo'
ACCESS_SECRET = '21QzW3EedeQnW6ctGjhFJdi48gjthWoCT53ReBUcejHHF'

api = tweepy.API(auth)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

mentions = api.mentions_timeline() #recent mentions

FILE_NAME = "last_seen_id"


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True) #what is flush
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended') #what are these params
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#mysanriokin' in mention.full_text.lower():
            print('found #mysanriokin!', flush=True)
            print('responding back...', flush=True)
            # get ID of user from tweet
            user_id = mention.author #test to see if this returns user id once you get developer
            character = character_from_user(user_id)
            #if statements to update status depending on character!

            api.update_status('@' + mention.user.screen_name +
                    '#HelloWorld back to you!', mention.id)

def character_from_user(user_id):
    """returns the sanrio character name based on tweet sentiments
    characters:
    - hello kitty: frineds, crazy
    - kuromi: edgy
    - chococat: curious, knowledge
    - keroppi: happy, friends
    - cinnamoroll: help, kind,
    - little twin stars: friends, help
    - my melody: shy, kind
    - pompompurin: kind, help, knowledge
    - mimmy: pretty, shy, kind
    - Badtz-Maru: crazy
    """
    # get string of last 20 tweets
    user_tweets = api.user_timeline(user_id)  # idk what to put in params, try to get more tweets tho
    # user_tweets = tweepy.Cursor(api.user_timeline, id=user_id).items() ALTERNATIVE??
    crazy = 0
    curious = 0
    knowledge = 0
    help = 0
    kind = 0
    happy = 0
    friends = 0
    edgy = 0
    shy = 0
    pretty = 0

    for tweet in user_tweets:  # what is reversed, should i do reversed???
        # count to see certain sentiments, certain use of words
        positivity = TextBlob(tweet.full_text).sentiment.polarity  # find a way to read the analysis
        #can we do autocorrect
        # find words
        if  'edge' in tweet.full_text or 'edgy' in in tweet.full_text:
            edgy += 1
        elif positivity > 0.5 or 'fun' in tweet.full_text or 'excite' in tweet.full_text or 'exciting' in tweet.full_text or 'pumped' in tweet.full_text or 'omg' in tweet.full_text or 'amazing' in tweet.full_text or 'happy' in in tweet.full_text:
            happy += 1
        elif 'wonder' in tweet.full_text or '?' in tweet.full_text or 'surprised' in tweet.full_text or 'huh' in tweet.full_text or 'wow' in tweet.full_text or 'curious' in tweet.full_text or 'know' in tweet.full_text:
            curious += 1

        # if statements for how many counts, then return the character


while True: #when would it be false tho
    reply_to_tweets()
    time.sleep(15)







