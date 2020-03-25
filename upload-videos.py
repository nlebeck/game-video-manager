# I will hopefully write some better documentation once I'm closer to finished.
# In the meantime, here are some notes for myself:
#
# * I work with local video files in the form of paths and video files in cloud
# storage as (name, timestamp, size) tuples.
#
# My main resource in writing this script was the Python documentation.
# Here are some other links that I found useful:
# https://stackoverflow.com/a/4172465
# https://stackoverflow.com/a/1504742

from datetime import datetime
import os
from pathlib import Path

CONFIG_FILE = 'config.txt'

# Indices of the different components of a video tuple
NAME_INDEX = 0
TIME_INDEX = 1
SIZE_INDEX = 2

def get_size_megabytes(path):
    return os.path.getsize(path) / (1024 * 1024)

def get_modification_time(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def datetime_to_string(datetime):
    return repr(datetime.year) \
        + '-' + repr(datetime.month) \
        + '-' + repr(datetime.day) \
        + '-' + repr(datetime.hour) \
        + '-' + repr(datetime.minute) \
        + '-' + repr(datetime.second)

def get_canonical_name(path):
    return user_name + '-' + datetime_to_string(get_modification_time(path)) + path.suffix

# Figure out which stored files to delete, in order to make space for all of
# the videos in upload_list. Returns a list of video names.
#
# Assumptions: get_stored_videos() returns videos sorted in ascending timestamp
# order.
#
# Preconditions: upload_list does not contain any videos in cloud storage.
#
def identify_stored_deletions(upload_list, storage_limit):
    upload_size = 0
    for path in upload_list:
        upload_size += get_size_megabytes(path)
    stored_videos = get_stored_videos()
    storage_size = 0
    for video in stored_videos:
        storage_size += video[SIZE_INDEX]
    total_size= upload_size + storage_size
    deletion_list = []
    index = 0
    while total_size > storage_limit:
        deletion_list.append(stored_videos[index][NAME_INDEX])
        total_size -= stored_videos[index][SIZE_INDEX]
        index += 1
    return deletion_list

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

# This is a 'mocked' version of the function.
#
# TODO: Implement this function for real.
#
def get_stored_videos():
    return mocked_stored_videos

# This is a 'mocked' version of the function.
#
# TODO Implement this function for real.
#
def remove_video(name):
    index = -1
    for i in range(0, len(mocked_stored_videos)):
        if mocked_stored_videos[i][NAME_INDEX] == name:
            index = i
    del mocked_stored_videos[index]

# This is a 'mocked' version of the function.
#
# TODO Implement this function for real.
#
def upload_video(path):
    name = get_canonical_name(path)
    time = get_modification_time(path)
    size = get_size_megabytes(path)
    mocked_stored_videos.append((name, time, size))

# These are variables used to simulate cloud storage for the mocked functions
# above.
#
# TODO Delete these variables when they're no longer needed.
#
mocked_stored_videos = [
    ('Niel-3-24-12-00-00.mkv', datetime(2020, 3, 24, 12, 00, 00), 200),
    ('Niel-3-24-12-10-00.mkv', datetime(2020, 3, 24, 12, 10, 00), 200)
]

config_params = read_config_params()
local_video_dir = config_params['LOCAL_VIDEO_DIR']
user_name = config_params['USER_NAME']
storage_limit = int(config_params['STORAGE_LIMIT_MB'])

p = Path(local_video_dir)

videos_to_upload = []
for x in p.iterdir():
    print(get_size_megabytes(x))
    print(get_canonical_name(x))
    videos_to_upload.append(x)

stored_videos = get_stored_videos()
for video in stored_videos:
    print(video[TIME_INDEX])
deletion_list = identify_stored_deletions(videos_to_upload, storage_limit)
print(deletion_list)
