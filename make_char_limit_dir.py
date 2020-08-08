import io
import os

charlim = 3000

parent_dir = '/Users/soumyadugg'
dir_name = 'legal_advice_files'
dir_path = os.path.join(parent_dir, dir_name + '_cleaned')

char_lim_dir = os.path.join(parent_dir, dir_name + '_charlim{}'.format(charlim))
if not os.path.isdir(char_lim_dir):
    os.mkdir(char_lim_dir)
#else delete all files in directory

k = 0
for i in range(600,720):
    for j in range(100):
        file = open(os.path.join(dir_path, 'doc{}-{}.txt'.format(i,j)), 'r')
        content = file.read()
        if len(content) >= charlim :
            #write to new directory
            new_file = open(os.path.join(char_lim_dir,'doc{}.txt'.format(k)), 'w')
            new_file.write(content)
            new_file.close()
            k+=1
        file.close()