import io
import os
import re

parent_dir = '/Users/soumyadugg'
#dir_names = ['legal_advice_files', 'legal_advice_files_cleaned'] #', legal_advice_files_charmin2000', 'legal_advice_files_charmin3000']
new_general_dir_path = os.path.join(parent_dir, 'legal_advice_data')
#if not os.path.exists(new_general_dir_path):
    #os.mkdir(new_general_dir_path)

#for dir_name in dir_names:

dir_name = 'legal_advice_files'
dir_path = os.path.join(parent_dir, dir_name)
new_dir_path = os.path.join(new_general_dir_path, dir_name + '_new')
if not os.path.exists(new_dir_path):
    os.mkdir(new_dir_path)

dirlist = ['doc{}-{}.txt'.format(i,j) for i in range(600,1224) for j in range(100)]

for file_name in dirlist:
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        continue

    file = open(file_path, 'r')
    content = file.read()
    pattern_mod = 'moderator(s?)'

    if re.search(pattern_mod, content) == None and len(content)>0:
        new_file = open(os.path.join(new_dir_path, file_name), 'w')
        new_file.write(content)
        new_file.close()

    file.close()
