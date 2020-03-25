import os
from pathlib import Path
import time

CONFIG_FILE = 'config.txt'

def get_size_megabytes(path):
    return os.path.getsize(path) / (1024 * 1024)

def get_modification_time(path):
    return time.gmtime(os.path.getmtime(path))

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

p = Path(video_dir)

for x in p.iterdir():
    print(get_size_megabytes(x))
    print(get_modification_time(x))
