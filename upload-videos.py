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

# Figures out which stored files to delete, in order to make space for all of
# the videos in upload_list. Returns a list of video tuples.
#
# Assumptions: get_stored_videos() returns videos sorted in ascending timestamp
# order.
#
# Preconditions: upload_list does not contain any videos in cloud storage.
#
def identify_stored_deletions(upload_list, stored_video_tuples, storage_limit):
    upload_size = 0
    for path in upload_list:
        upload_size += get_size_megabytes(path)
    storage_size = 0
    for video in stored_video_tuples:
        storage_size += video[SIZE_INDEX]
    total_size = upload_size + storage_size
    deletion_list = []
    index = 0
    while total_size > storage_limit:
        deletion_list.append(stored_video_tuples[index])
        total_size -= stored_video_tuples[index][SIZE_INDEX]
        index += 1
    return deletion_list

# Figures out which local videos are not stored in cloud storage and are newer
# than any of the videos in cloud storage. Returns a list of paths.
#
def identify_new_local_videos(local_video_paths, stored_video_tuples):
    stored_video_names = []
    for video in stored_video_tuples:
        stored_video_names.append(video[NAME_INDEX])
    last_stored_timestamp = stored_video_tuples[len(stored_videos) - 1][TIME_INDEX]
    new_video_paths = []
    for path in local_video_paths:
        name = get_canonical_name(path)
        timestamp = get_modification_time(path)
        if stored_video_names.count(name) == 0 and timestamp > last_stored_timestamp:
            new_video_paths.append(path)
    return new_video_paths

# Figures out which local videos are currently stored in cloud storage, or are older
# than any video in cloud storage, and can be safely deleted. Returns a list of paths.
#
def identify_old_local_videos(local_video_paths, stored_video_tuples):
    stored_video_names = []
    for video in stored_video_tuples:
        stored_video_names.append(video[NAME_INDEX])
    oldest_stored_timestamp = stored_video_tuples[0][TIME_INDEX]
    old_video_paths = []
    for path in local_video_paths:
        name = get_canonical_name(path)
        timestamp = get_modification_time(path)
        if stored_video_names.count(name) or timestamp < oldest_stored_timestamp:
            old_video_paths.append(path)
    return old_video_paths

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
def remove_stored_video(video_tuple):
    mocked_stored_videos.remove(video_tuple)

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

local_videos = []
for x in p.iterdir():
    local_videos.append(x)

stored_videos = get_stored_videos()
print('Printing stored videos:')
print(stored_videos)
new_videos = identify_new_local_videos(local_videos, stored_videos)
deletion_list = identify_stored_deletions(new_videos, stored_videos, storage_limit)
print('Deleting old videos from the cloud...')
for video_tuple in deletion_list:
    print('Deleting video ' + video_tuple[NAME_INDEX])
    remove_stored_video(video_tuple)
print('Uploading new videos...')
for path in new_videos:
    print('Uploading video ' + path.name + ' of size ' + repr(round(get_size_megabytes(path), 1)) + ' MB')
    upload_video(path)
print('Printing stored videos again:')
print(get_stored_videos())

print('Identifying local videos that can be deleted: ')
old_videos = identify_old_local_videos(local_videos, stored_videos)
print(old_videos)
