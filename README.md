# Game Video Manager

I'm working on a set of scripts to simplify sharing video recordings from PC
games. The plan is to have one script that uploads each user's most recent
videos to an AWS storage bucket and another script that downloads all new
videos from the bucket. The scripts would enforce a per-user maximum storage
budget, to keep the total AWS storage usage capped.

The immediate use case for this project is for a group of friends playing video
games together, where one person makes "highlight reel" videos. The point is to
make it easy for everyone to record their gameplay and then share their videos
with that one person.

## Setup

These setup instructions are for the current version of this script, which uses
a shared OneDrive folder as the storage backend.

1. Install Python 3: https://www.python.org/.

2. Set up your video recording software to put all recordings in the same
folder, and make sure there are no non-video files in that folder.

3. Make sure the OneDrive client is installed, log into your OneDrive account,
and make sure the shared folder is showing up on your local filesystem.

4. Download `upload-videos.py` and `config.txt` from this repository, and put
them in the same folder (it doesn't matter where they are, as long as they're
in the same folder).

5. Edit `config.txt` to fill in the missing settings. `LOCAL_VIDEO_DIR` should
be the path to the folder where your recording software puts recordings,
`USER_NAME` should be your first name or nickname (no spaces), and
`ONEDRIVE_VIDEO_DIR` should be the path to the shared OneDrive folder on your
local filesystem. Make sure `STORAGE_LIMIT_MB` is set to the number we agreed
on. You can change `DELETE_LOCAL_VIDEOS` from "no" to "yes" if you want the
script to delete videos from your local folder after it uploads them to
cloud storage.