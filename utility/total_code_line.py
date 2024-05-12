import os
import glob
import operator

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
extensions = ['*.py', '*.bat']
ignore_paths = [
    './backtester/graph',
    './backtester/temp',
    './lecture/imagefiles',
    './lecture/testcode/temp',
    './_database',
    './pycharm'
    './.git',
    './.idea',
    './__pycache__',
    './_log',
    './icon'
]

total_line_count = 0
total_file_count = 0
files_grabbed = []

line_count_dict = {}
extension_count_dict = dict.fromkeys(extensions, 0)
[files_grabbed.extend(glob.glob(f'{ROOT_DIR}/**/{extension}', recursive=True)) for extension in extensions]

for file_name_with_path in files_grabbed:
    file_name = file_name_with_path.split('/')[-1]
    ext = file_name.split('.')[-1]
    is_ignored = False
    for ignore_path in ignore_paths:
        if file_name_with_path.find(ignore_path) != -1:
            is_ignored = True
            break
    if is_ignored:
        continue
    extension_count_dict['*.' + ext] += 1
    line_count = len(open(file_name_with_path, encoding='ISO-8859-1').readlines())
    line_count_dict[file_name_with_path] = line_count
    total_line_count += line_count
    total_file_count += 1
sorted_line_count = sorted(line_count_dict.items(), key=operator.itemgetter(1), reverse=True)

for file, count in sorted_line_count:
    print('{:>5} {}'.format(count, file))

print(f'\n프로젝트 전체 파일 수 :   {total_file_count} 개')
print(f'프로젝트 전체 라인 수 : {total_line_count} 줄')
