#!/usr/bin/python3
###############################################################################
#    ___  ___          _            _              ______            _        #
#    |  \/  |         | |          | |             | ___ \          | |       #
#    | .  . | __ _ ___| |_ __ _  __| | ___  _ __   | |_/ / __ _  ___| | __    #
#    | |\/| |/ _` / __| __/ _` |/ _` |/ _ \| '_ \  | ___ \/ _` |/ __| |/ /    #
#    | |  | | (_| \__ \ || (_| | (_| | (_) | | | | | |_/ / (_| | (__|   <     #
#    \_|  |_/\__,_|___/\__\__,_|\__,_|\___/|_| |_| \____/ \__,_|\___|_|\_\    #
###############################################################################
# Title           : mastodonposts.py                                          #
# Description     : Backups User Personal Mastodon Posts                      #
# Authot          : Creeva                                                    #
# Date            : 2-16-2025                                                 #
# Version         : 1.0                                                       #
# Notes           : https://github.com/creeva/discordjane'                    #
###############################################################################
# Version History                                                             #
#       Version   : 1.0 - Initial Version                                     #
###############################################################################
# Script Setup                                                                #
###############################################################################
#
import glob
import os
from mastodon import Mastodon
#
###############################################################################
# Variables                                                                   #
###############################################################################
#
# Mastodon Connection Information
#
access_token='APIACCESSTOKENGOESHERE'
api_base_url= 'SERVERURLGOESHERE'
mastodon = Mastodon(access_token=f'{access_token}', api_base_url=f'{api_base_url}')
# Mastodon Information
userid = mastodon.account_verify_credentials()['id']
avatar = mastodon.account_verify_credentials()['avatar']
bio = mastodon.account_verify_credentials()['note']
bot = mastodon.account_verify_credentials()['bot']
creation = mastodon.account_verify_credentials()['created_at']
displayname = mastodon.account_verify_credentials()['display_name']
discoverable = mastodon.account_verify_credentials()['discoverable']
following = mastodon.account_verify_credentials()['following_count']
followers = mastodon.account_verify_credentials()['followers_count']
followerlist = mastodon.account_followers(userid)
followinglist = mastodon.account_following(userid)
group = mastodon.account_verify_credentials()['group']
header = mastodon.account_verify_credentials()['header']
publicfollowed = mastodon.account_verify_credentials()['locked']
statuscount = mastodon.account_verify_credentials()['statuses_count']
url = mastodon.account_verify_credentials()['url']
username = mastodon.account_verify_credentials()['username']
# Mastodon Post Info
all_posts = []
max_id = None
api_base_url = api_base_url.replace('https://', '')
api_base_url = api_base_url.replace('http://', '')
#
###############################################################################
# Main Script Start                                                           #
###############################################################################
#
# Directory Checking and Creation
#
if not glob.glob('socialposts'): os.makedirs('socialposts')
if not glob.glob('socialreports'): os.makedirs('socialreports')
if glob.glob(f'socialposts/mastodon-{username}-{api_base_url}-posts.txt'): os.remove(f'socialposts/mastodon-{username}-{api_base_url}-posts.txt')
if glob.glob(f'socialreports/mastodon-{username}-{api_base_url}-report.txt'): os.remove(f'socialreports/mastodon-{username}-{api_base_url}-report.txt')
# Loop to retrieve all posts, handling pagination
while True:
    posts = mastodon.account_statuses(userid, limit=40, max_id=max_id)
    if not posts:
        break 
    all_posts.extend(posts)
    max_id = posts[-1]['id'] - 1
# Process or save the retrieved posts (e.g., save to a file)
for post in all_posts:
    postfile = f'socialposts/mastodon-{username}-{api_base_url}-posts.txt'
    with open(postfile, mode='a', encoding='utf8') as infile: 
        infile.write(f"\n{post['created_at']}   --   MASTODON   --   {username}   --   {api_base_url}   --   {post['id']}   --   {post['content']}")
# Account Report
reportfile = f'socialreports/mastodon-{username}-{api_base_url}-report.txt'
with open(reportfile, mode='a', encoding='utf8') as infile: 
    infile.write('\nMastadon Account Report\n\n')
    infile.write(f'\nUsername          : {username}')
    infile.write(f'\nDisplay Name      : {displayname}')
    infile.write(f'\nMastadon Server   : {api_base_url}')
    infile.write(f'\nNumerical ID      : {userid}')
    infile.write(f'\nCreated On        : {creation}')
    infile.write(f'\nBio               : {bio}')
    infile.write(f'\nURL               : {url}')
    infile.write(f'\nAvatar            : {avatar}')
    infile.write(f'\nHeader            : {header}')
    infile.write(f'\nStatus Count      : {statuscount}')
    infile.write(f'\nFollowing Count   : {following}')
    infile.write(f'\nFollowers Count   : {followers}')
    infile.write(f'\nFollowable by All : {publicfollowed}')
    infile.write(f'\nBot               : {bot}')
    infile.write(f'\nDiscoverable      : {discoverable}')
    infile.write(f'\nGroup             : {group}')
    for following in followinglist:
        printfollower = following['username']
        infile.write(f'\nFollowing         : {printfollower}')
    for follower in followerlist:
        printfollower = follower['username']
        infile.write(f'\nFollower          : {printfollower}')
