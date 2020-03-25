# My main resource in writing this script was the Python documentation.
# Here are some other links that I found useful:
# https://stackoverflow.com/a/4172465

import os
from pathlib import Path
import time

CONFIG_FILE = 'config.txt'

def get_size_megabytes(path):
    return os.path.getsize(path) / (1024 * 1024)

def get_modification_time(path):
    return time.gmtime(os.path.getmtime(path))

def struct_time_to_string(time):
    return repr(time.tm_year) \
        + '-' + repr(time.tm_mon) \
        + '-' + repr(time.tm_mday) \
        + '-' + repr(time.tm_hour) \
        + '-' + repr(time.tm_min) \
        + '-' + repr(time.tm_sec)

def get_canonical_name(path):
    return user_name + '-' + struct_time_to_string(get_modification_time(path)) + path.suffix

def read_config_params():
    config_dict = dict()
    config_file = open(CONFIG_FILE)
    for line in config_file:
        stripped_line = line.rstrip()
        split = stripped_line.split('=')
        key = split[0]
        val = split[1]
        config_dict[key] = val
    return config_dict

config_params = read_config_params()
video_dir = config_params['VIDEO_DIR']
user_name = config_params['USER_NAME']

p = Path(video_dir)

for x in p.iterdir():
    print(get_size_megabytes(x))
    print(get_canonical_name(x))
