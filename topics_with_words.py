import sys
import getopt
import io
import os
import pandas as pd
import matplotlib as mlib

input_topic_state = ''
new_dir_name = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "odir="])
except getopt.GetoptError:
    print('topics_with_words.py -i <inputfile> -o <outputdir>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('topics_with_words.py -i <inputfile> -o <outputdir>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        input_topic_state = arg
    elif opt in ("-o", "--odir"):
        new_dir_name = arg

parent_dir = '/Users/soumyadugg/reddit_topic_modeling/'
topics_dir = os.path.join(parent_dir, new_dir_name)
os.mkdir(topics_dir)

df = pd.read_csv(input_topic_state, delimiter = ' ', comment = '#', skiprows = 1)
topics_words_table = df[['topic', 'type']]
topics_words_table = topics_words_table.drop_duplicates()
by_topic = topics_words_table.groupby('topic')

for topic, frame in by_topic:
    f = open(os.path.join(topics_dir, 'topic-{}.txt'.format(str(topic))), 'w')
    f.write('Topic Number ' + str(topic) + '\n\n')
    for word in frame['type']:
        f.write(str(word)+'\n')

