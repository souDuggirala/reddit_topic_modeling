import json
import requests
import time
import re
import os

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


def makeThreadList(submissionlist):
    
    def makeThreadEntry(submission):
        thread = []

        try:
            thread.append(submission['selftext'])
        except KeyError:
            print('Here is the submission that failed: \n\n')
            print(json.dumps(submission, indent = 4))

        
        payload = {'fields': 'body', 'size': submission['num_comments'],'link_id': submission['id'],'author':'!LocationBot','mod_removed':'false'}
        comments = makeRequest('https://api.pushshift.io/reddit/search/comment/', payload)
        for i in range(len(comments['data'])):
            thread.append(comments['data'][i]['body'])
        return thread
    
    threads = []
    for j in range(len(submissionlist)):
        thread_j = makeThreadEntry(submissionlist[j])
        threads.append(thread_j)
    return threads


def preprocess(threadlist):
    
    def clean(threadlist):
        for i in range(len(threadlist)):
            #delete urls
            pattern_url = r'https://[\w/#:?._~-]*'
            for j in range(len(threadlist[i])):
                threadlist[i][j] = re.sub(pattern_url,'', threadlist[i][j])
        
            #replace quoted stuff, &gt;[a-zA-Z0-9?.,:;() ]\n\n with whitespace
            #doesn't always have to end in \n\n, if it doesn't, just delete until sentence ends
            pattern_quoted = r'&gt;([\w\s’.?/,()]*\n\n|[\w\s’/,()]*)'
            for j in range(len(threadlist[i])):
                threadlist[i][j] = re.sub(pattern_quoted,' ', threadlist[i][j])
            
            #replace \n or \n\n&amp;#x200B;\n\n or \n\n or &amp; or \n-\t with white space
            pattern_spaces = r'(\n|(&amp;(#x200B;)?)|-\t)+'
            for j in range(len(threadlist[i])):
                threadlist[i][j] = re.sub(pattern_spaces,' ', threadlist[i][j])
    
            #delete stars
            pattern_stars = r'(\*)+'
            for j in range(len(threadlist[i])):
                threadlist[i][j] = re.sub(pattern_stars,'', threadlist[i][j])
           
            #reduce all multiple whitespaces to 1
            pattern_whitespace = r'(\s)+'
            for j in range(len(threadlist[i])):
                threadlist[i][j] = re.sub(pattern_whitespace,' ', threadlist[i][j])
            
    def deleteIrrelevantComments(threadlist):
        mod_pattern = 'Do not reach out to a moderator personally, and do not reply to this message as a comment.'
        for i in range(len(threadlist)):
            j = 0
            while j < len(threadlist[i]):
                if (threadlist[i][j]=='[removed]' or threadlist[i][j]=='[deleted]' or re.search(mod_pattern,threadlist[i][j]) != None or len(threadlist[i][j])==0):
                    del threadlist[i][j]
                j+=1
    
    deleteIrrelevantComments(threadlist)
    clean(threadlist)

def makeTextFiles(threadlist, directory, nextStartNum):
    dir_name = '/Users/soumyadugg/reddit_topic_modeling/' + directory
    
    for i in range(len(threadlist)):
        crnt_file = os.path.join(dir_name, 'doc'+ str(nextStartNum + i)+'.txt')
        f = open(crnt_file, 'w')
        
        #should already be edited
        for j in range(len(threadlist[i])):
            f.write(' ' + threadlist[i][j])
        
        f.close()


uri = 'https://api.pushshift.io/reddit/search/submission/'
subreddit = 'legaladvice'
dir_name = 'legal_advice_files'
payload = {'fields': ['id','num_comments','selftext'],'subreddit': subreddit, 'size': 100,'author':'!LocationBot','mod_removed':'false', 'before':'','after':''}
for i in range(50):
    print(str(i))
    payload['before'] = str(600+(2*i))+'d'
    payload['after'] = str(600+(2*i))+'d'
    submissionlist = makeRequest(uri, payload)
    threadlist = makeThreadList(submissionlist['data'])
    preprocess(threadlist)
    makeTextFiles(threadlist,dir_name,3000+i*100)