# I will hopefully write some better documentation once I'm closer to finished.
# In the meantime, here are some notes for myself:
#
# * I work with local video files in the form of paths and video files in cloud
# storage as (name, timestamp, size) tuples.
#
# * I am going to just use a shared OneDrive folder as the storage backend for
# now.
#
# My main resource in writing this script was the Python documentation.
# Here are some other links that I found useful:
# https://stackoverflow.com/a/4172465
# https://stackoverflow.com/a/1504742

from datetime import datetime
import os
from pathlib import Path
import shutil
import sys

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
    if len(stored_video_tuples) == 0:
        return []

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
    if len(stored_video_tuples) == 0:
        return local_video_paths.copy()

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
    if len(stored_video_tuples) == 0:
        return []

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

def delete_local_video(path):
    path.unlink()

def calculate_total_size_megabytes(video_tuple_list):
    total_size = 0
    for video_tuple in video_tuple_list:
        total_size += video_tuple[SIZE_INDEX]
    return total_size

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

def get_local_videos():
    local_videos = []
    dir_path = Path(local_video_dir)
    for path in dir_path.iterdir():
        local_videos.append(path)
    return local_videos

# Check if the videos to upload are larger than the storage limit by
# themselves.
# Currently, this function just returns a boolean value, since the script will
# just exit if the upload list is too large to fit.
#
def validate_upload_list(upload_list, storage_limit):
    total_size = 0
    for path in upload_list:
        total_size += get_size_megabytes(path)
    return total_size <= storage_limit


# These functions are part of the 'public' storage interface. Their
# implementation currently uses a shared OneDrive folder as the storage
# backend.

def get_stored_videos(user_name):
    onedrive_dir = get_onedrive_dir_path(user_name)
    video_tuples = []
    for path in onedrive_dir.iterdir():
        name = path.name
        timestamp = get_timestamp_from_canonical_name(name, user_name)
        size = get_size_megabytes(path)
        video_tuples.append((name, timestamp, size))
    return sorted(video_tuples, key = get_video_tuple_timestamp)

# I think I need to define this function explicitly to sort a list of video
# tuples by timestamp, but I'm not sure.
def get_video_tuple_timestamp(video_tuple):
	return video_tuple[TIME_INDEX]

def remove_stored_video(video_tuple):
    path = get_onedrive_dir_path().joinpath(video_tuple[NAME_INDEX])
    path.unlink()

def upload_video(path):
    name = get_canonical_name(path)
    dest_path = get_onedrive_dir_path().joinpath(name)
    shutil.copyfile(str(path), str(dest_path))


# These functions are used internally to implement the storage interface above.

def get_onedrive_dir_path(user_name):
    config_params = read_config_params()
    base_path_string = config_params['ONEDRIVE_VIDEO_DIR']
    base_path = Path(base_path_string)
    user_path = base_path.joinpath(user_name)
    return Path(user_path)

def init_storage(user_name):
    path = get_onedrive_dir_path(user_name)
    if not path.exists():
        os.mkdir(str(path))

def get_timestamp_from_canonical_name(name, user_name):
    split = name.split('.')
    ts_string = split[0][(len(user_name) + 1):]
    ts_split = ts_string.split('-')
    timestamp = datetime(year = int(ts_split[0]),
                         month = int(ts_split[1]),
                         day = int(ts_split[2]),
                         hour = int(ts_split[3]),
                         minute = int(ts_split[4]),
                         second = int(ts_split[5])
                        )
    return timestamp

config_params = read_config_params()
local_video_dir = config_params['LOCAL_VIDEO_DIR']
user_name = config_params['USER_NAME']
storage_limit = int(config_params['STORAGE_LIMIT_MB'])
delete_local = False
if config_params['DELETE_LOCAL_VIDEOS'] == 'yes':
    delete_local = True

init_storage(user_name)

local_videos = get_local_videos()
stored_videos = get_stored_videos(user_name)

print('Your cloud storage usage before running this script: ', end = '')
print(repr(round(calculate_total_size_megabytes(stored_videos), 1)) + ' MB')

new_videos = identify_new_local_videos(local_videos, stored_videos)
validation_result = validate_upload_list(new_videos, storage_limit)
if not validation_result:
    print()
    print('ERROR: Your new videos by themselves overflow your storage limit.')
    print('Go delete some videos from your local video directory and try')
    print('running this script again.')
    print()
    print('In theory, this script could just upload the most recent new')
    print('videos that stay under the limit, but Niel was too lazy to')
    print('implement that functionality. Go heckle him if you want this')
    print('feature implemented.')
    print()
    input('Press any key to exit.')
    sys.exit(1)

deletion_list = identify_stored_deletions(new_videos, stored_videos, storage_limit)
print('Deleting old videos from cloud storage if necessary...')
for video_tuple in deletion_list:
    print('Deleting video ' + video_tuple[NAME_INDEX])
    remove_stored_video(video_tuple)
print('Uploading new videos from your local storage...')
for path in new_videos:
    print('Uploading video ' + path.name + ' of size ' + repr(round(get_size_megabytes(path), 1)) + ' MB')
    upload_video(path)

# Refresh the cached copy of the stored video list
stored_videos = get_stored_videos(user_name)

print('Your updated cloud storage usage: ', end = '')
print(repr(round(calculate_total_size_megabytes(stored_videos), 1)) + ' MB')

if delete_local:
    print('Deleting old local videos... ')
    old_videos = identify_old_local_videos(local_videos, stored_videos)
    for path in old_videos:
        print('Deleting video ' + path.name)
        delete_local_video(path)

input('Press any key to exit.')