import io
import os

charmin = 2000

parent_dir = '/Users/soumyadugg'
dir_name = 'legal_advice_files'
dir_path = os.path.join(parent_dir, dir_name + '_cleaned')

char_min_dir = os.path.join(parent_dir, dir_name + '_charmin{}'.format(charmin))
if not os.path.isdir(char_min_dir):
    os.mkdir(char_min_dir)

k = 0
for i in range(600,1223):
    for j in range(100):
        file_path = os.path.join(dir_path, 'doc{}-{}.txt'.format(i,j))
        if not os.path.exists(file_path):
            continue
        file = open(file_path, 'r')
        content = file.read()
        if len(content) >= charmin :
            new_file = open(os.path.join(char_min_dir,'doc{}.txt'.format(k)), 'w')
            new_file.seek(0)
            new_file.truncate(0)
            new_file.write(content)
            new_file.close()
            k+=1
        file.close()