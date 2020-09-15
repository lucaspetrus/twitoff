"""Retrieve Tweets, embeddings, and persist in the database."""
from os import getenv
import basilica
import tweepy
from .models import DB, Tweet, User

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_API_KEY = getenv('WqBA9blzakJogGRAFT9K06RZ6')
TWITTER_API_KEY_SECRET = getenv('sftM99bgpCti0JYMGgIDMWRlZTV7ccBIECvwFHAvWt654rJ93D')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(getenv('223da4a6-be48-bc4b-8892-7c219e1b0906'))


def add_or_update_user(username):
    try:
        # grabbing twitter user
        twitter_user = TWITTER.get_user(username)
        # add or update user
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # grabbing tweet
        tweets = twitter_user.timeline(count=200, exclude_replies=True,
                                       include_rts=False, tweet_mode='Extended',
                                       since_id=db_user.newest_tweet_id)

        # if we get a new tweet then change the newest_tweet_id associated with ther user
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # loops for tweets
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print('ERROR PROCESSING {}: {}'.format(username, e))


DB.session.commit()


# populations using add_or_update user
def insert_example_users():
    add_or_update_user('elonmusk')
    add_or_update_user('KenJennings')
    add_or_update_user('nasa')
    add_or_update_user('IAM_SHAKESPEARE')
    add_or_update_user('conanobrien')
    add_or_update_user('common_squirrel')
    add_or_update_user('sadserver')
    add_or_update_user('jkhowland')
    add_or_update_user('calebhicks')
    add_or_update_user('rrherr')
    add_or_update_user('SteveMartinToGo')
    add_or_update_user('alyankovic')
    add_or_update_user('big_ben_clock')
    add_or_update_user('austen')


DB.session.commit()


# FLASK_APP=twitoff:APP flask run
