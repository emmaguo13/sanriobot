
#get photos
#upload to github
#test bot
#release bot
import tweepy, nltk, pandas, os, time
from textblob import TextBlob
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#twitter credentials
CONSUMER_KEY = 'I9tO6b8wMWeL8zcSiL73KM6sQ'
CONSUMER_SECRET = 'jUHEiAx7NnuIa5Vz9Hy81VrQHODus2m5yyVOd5EG6moXgUlPFo'
ACCESS_KEY = '1267989567484817410-BpjfAOvFyyUon7EF6AYbzIpnSBoxyF'
ACCESS_SECRET = '5qLH97G9t63JHmMQ9kKBtX8JtJiYIImVO5NIWSJSzg7MT'

#personality credentials
personality_api = "v0NlU-NxanvPSGaF-Dy9XmuT_7OAP3ahoJxpy3F_L0lY"
personality_url = 'https://api.us-south.personality-insights.watson.cloud.ibm.com/instances/406c243e-5b13-4d34-810f-c33226482893'

#twitter authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

mentions = api.mentions_timeline() #recent mentions

FILE_NAME = "last_seen_id"

#personality authentication
auth_personality = IAMAuthenticator(personality_api) #instance of personality thing
personality_insights = PersonalityInsightsV3(version = '2-17-10-13',
                                             authenticator = auth_personality)
personality_insights.set_service_url(personality_url) #where our personality thing is



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
            username = mention.user.screen_name
            path = character_from_user(username)
            api.update_with_media(path, '@' + mention.user.screen_name + ' hi'
                  , mention.id)

def character_from_user(username):
    """returns the sanrio character name based on tweet sentiments
    characters:
    - hello kitty: openness, agreeableness
    - kuromi: challenge, excitement
    - chococat: conscientiousness and agreeabeness, curiosity
    - keroppi: extraversion
    - cinnamoroll: emotion
    - little twin stars: closeness -
    - my melody: love, extroverted
    - pompompurin: excitementt -
    - mimmy: conscientiouss
    """
    # get last 1000 tweets, join the text together
    user_tweets = api.user_timeline(username, count = 100, include_rts = True)
    tweets_text = [tweet.text for tweet in user_tweets]
    joined_text = ''.join(str(tweet) for tweet in tweets_text)

    #analyze the text
    analysis_profile = personality_insights.profile(joined_text, accept ='application/json' ).get_result()
    for personality in analysis_profile['personality']:
        if personality['name'] == 'Openness':
            openness = personality['percentile']
        elif personality['name'] == 'Conscientiousness':
            conscientiousness = personality['percentile']
        elif personality['name'] == 'Extraversion':
            extraversion = personality['percentile']
        elif personality['name'] == 'Agreeableness':
            agreeableness = personality['percentile']
        elif personality['name'] == 'Emotional Range':
            emotion = personality['percentile']

    for personality in analysis_profile['needs']:
        if personality['name'] == 'Challenge':
            challenge = personality['percentile']
        elif personality['name'] == 'Closeness':
            closeness = personality['percentile']
        elif personality['name'] == 'Curiosity':
            curiosity = personality['percentile']
        elif personality['name'] == 'Excitement':
            excitement = personality['percentile']
        elif personality['name'] == 'Love':
            love = personality['percentile']

    if openness >= 0.50 and agreeableness >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/HelloKitty.jpg"
    elif challenge >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Kuromi.jpg"
    elif curiosity >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Chococat.jpg"
    elif extraversion >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Keroppi.png"
    elif emotion >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Cinnamoroll.jpg"
    elif closeness >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/LittleTwinStars.jpg"
    elif love >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/MyMelody.jpg"
    elif excitement >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Pompompurin.png"
    elif conscientiousness >= 0.50:
        return "/Users/emmaguo/sanriobot/photos/Mimmy.gif"
    else:
        return "/Users/emmaguo/sanriobot/photos/HelloKitty.jpg"


while True: #when would it be false tho

    reply_to_tweets()
    time.sleep(15)







