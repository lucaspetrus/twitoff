
"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    embedding = DB.Column(DB.PickleType, nullable=False)

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


#def insert_example_users():
    #"""Example data to play with."""
    #austen = User(id=1, name='austen')
    #elon = User(id=2, name='elonmusk')
    #rherr = User(id=3, name='rrherr')
    #stevemartin = User(id=4, name='SteveMartinToGo')
    #alyankovic = User(id=5, name='alyankovic')
    #nasa = User(id=6, name='nasa')
    #caleb = User(id=7, name='calebhicks')
    #sadserver = User(id=8, name='sadserver')
    #jkhowland = User(id=9, name='jkhowland')
    #squirrel = User(id=10, name='common_squirrel')
    #kenjennings = User(id=11, name='KenJennings')
    #conanobrien = User(id=12, name='conanobrien')
    #bigbenclock = User(id=13, name='big_ben_clock')
    #iamshakespeare = User(id=14, name='IAM_SHAKESPEARE')
    #DB.session.add(austen)
    #DB.session.add(elon)
    #DB.session.add(nasa)
    #DB.session.add(rherr)
    #DB.session.add(stevemartin)
    #DB.session.add(alyankovic)
    #DB.session.add(caleb)
    #DB.session.add(sadserver)
    #DB.session.add(jkhowland)
    #DB.session.add(squirrel)
    #DB.session.add(kenjennings)
    #DB.session.add(conanobrien)
    #DB.session.add(bigbenclock)
    #DB.session.add(iamshakespeare)

    #DB.session.commit()

