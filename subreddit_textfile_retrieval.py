import json
import requests
import time
import re
import os
import io
#import emoji

def makeRequest(uri, payload, max_retries = 5):
    def fire_away(uri):
        response = requests.get(uri, payload)
        assert response.status_code == 200
        return json.loads(response.content)
    
    current_tries = 1
    while (current_tries < max_retries):
        try:
            time.sleep(1)
            return fire_away(uri)
        except:
            time.sleep(1)
            current_tries+=1
    
    return fire_away(uri)

#get list of subreddit posts
#for each subreddit post, get the comments
    #write the comments into a textfile with the submission, excluding comments from moderators/bots
#clean the resulting textfiles

def makeTextFiles(submissionlist, dir_path, after):
    def deleteIrrelevantComments(commentlist):
        pattern_mod = 'Do not reach out to a moderator personally|I am a bot, and this action was performed automatically'
        j = 0
        while j < len(commentlist['data']):
            if (re.search(pattern_mod,commentlist['data'][j]['body']) != None or len(commentlist['data'][j]['body'])==0):
                del commentlist['data'][j]
            j+=1

    #assumes f is open
    def makeTextFile(submission,f):
        payload = {'fields': 'body', 'size': submission['num_comments'],'link_id': submission['id'],'author':'!LocationBot','mod_removed':'false'}
        commentlist = makeRequest('https://api.pushshift.io/reddit/search/comment/', payload)
        deleteIrrelevantComments(commentlist)
        f.write(submission['selftext'])
        for i in range(len(commentlist['data'])):
            #write to textfile
            f.write(' ' + commentlist['data'][i]['body'])
        
    
    for j in range(len(submissionlist['data'])):
        filepath = os.path.join(dir_name, 'doc{}-{}.txt'.format(after,j))
        f = open(filepath, 'w')
        makeTextFile(submissionlist['data'][j], f)
        f.close()

def cleanFiles(dir_path, dir_name, parent_dir, request_size, after):
    cleaned_dir_path = os.path.join(parent_dir, dir_name + '_cleaned')
    if not os.path.isdir(cleaned_dir_path):
        os.mkdir(cleaned_dir_path)
    
    dirlist = ['doc{}-{}.txt'.format(after,i) for i in range(request_size)]

    for filename in dirlist:
        file = open(os.path.join(dir_path,filename), 'r')
        content = file.read()
        
        content = content.lower()

        #delete quotes
        #pattern_quoted = r'&gt;([\w\s’\'.?/,()]*\n\n|[\w\s’\'/,()]*)'
        #pattern_quoted = r'&gt;([\w\s’\'.?/,()]*\n)'
        #content = re.sub(pattern_quoted,' ', content)
        
        #delete urls
        pattern_url = r'http(s?)://[\w/#\\:?._~-]*'
        content = re.sub(pattern_url,' ', content)

        #delete [removed], [deleted]
        pattern_removed = r'\[removed\]|\[deleted\]'
        content = re.sub(pattern_removed, ' ', content)

        #delete subreddit titles
        pattern_subreddit = r'r/\w*'
        content = re.sub(pattern_subreddit,' ', content)

        pattern_html = r'&gt;|&lt;|&ge;|&le;|(&amp;(#x200B;)?)'
        content = re.sub(pattern_html,' ', content)

        #strip 's and (s)
        pattern_s = r'(\'|’)s|\(s\)'
        content = re.sub(pattern_s,' ', content)

        #delete punctuation
        pattern_symbols = r'(\*|\[|\]|\(|\)|-|/|\.(\.)+|,|\?)+'
        content = re.sub(pattern_symbols,' ', content)

        #delete words with that end with 't, 've, 're, 'll
        pattern_contractions = r'\w*(\'|’)(t|ve|re|ll|d)'
        content = re.sub(pattern_contractions,' ', content)

        #reduce all multiple whitespaces to 1
        pattern_whitespace = r'(\s)+'
        content = re.sub(pattern_whitespace,' ', content)

        new_file = open(os.path.join(cleaned_dir_path, filename), 'w')
        new_file.seek(0)
        new_file.truncate(0)
        new_file.write(content)
        
        new_file.close()
        file.close()


parent_dir = '/Users/soumyadugg/reddit_topic_modeling'
dir_name = 'legal_advice_files'
dir_path = os.path.join(parent_dir, dir_name)
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

uri = 'https://api.pushshift.io/reddit/search/submission/'
subreddit = 'legaladvice'
request_size = 100
payload = {'fields': ['id','num_comments','selftext'],'subreddit': subreddit, 'size': request_size,'author':'!LocationBot','mod_removed':'false','after':''}
for i in range(4):
    after = str(600+i)
    print(after)
    payload['after'] = after+'d'
    submissionlist = makeRequest(uri, payload)
    makeTextFiles(submissionlist, dir_path, after)
    cleanFiles(dir_path, dir_name, parent_dir, request_size, after)
