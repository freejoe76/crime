#!/usr/bin/env python
# Tweeter helps us tweet. Right now it just logs in, but that's not forever.
from twython import Twython
from twython import TwythonError, TwythonAuthError
import os, string


def write_file(content, filename):
    try:
        fn = open(filename, 'w')
        fn.write(content.encode('utf-8'))
    except IOError as inst:
        print type(inst), inst.args
        return False
    fn.close

def read_file(filename):
    try:
        fn = open(filename, 'r')
        content = fn.read()
        fn.close
    except IOError as inst:
        print type(inst), inst.args
        return False
    return content



if __name__ == '__main__':
    # Get the credentials we need to start tweeting.
    app_file = read_file('.appdata')
    oauth_file = read_file('.oauthdata')
    app_key = app_file.rsplit('|')[0]
    app_secret = app_file.rsplit('|')[1]
    oauth_token = oauth_file.rsplit('|')[0]
    oauth_token_secret = oauth_file.rsplit('|')[1]
    twitter = Twython(app_key=app_key,
                app_secret=app_secret,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret)



