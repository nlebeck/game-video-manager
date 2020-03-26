# Game Video Manager

This repository contains a script that simplifies sharing recent video
recordings using cloud storage. The script identifies new videos stored locally
and uploads them to cloud storage, optionally deleting the local copies after
uploading them. It enforces a per-user maximum storage budget and deletes your
oldest stored videos to make space for newer ones.

Currently, this script uses OneDrive as the cloud storage backend and requires
you to run the OneDrive client to map a shared folder onto your local
filesystem. (It would probably work with something similar, like Google Drive
or Dropbox, without any changes.) If you wanted to, you could manually copy
your latest video recordings into the OneDrive folder, delete old recordings
from OneDrive to free up space, organize and name the videos, and so on. Think
of this script as a way to do all of that automatically, with a single click.

## Warnings

I have done some testing, and this script generally seems to be working
correctly. However, there are still plenty of things that could go wrong:

* This script could accidentally delete a video, especially if you have the
`DELETE_LOCAL_VIDEOS` option enabled. If you did something really awesome on
your latest recording, consider making your own backup of the file before
running this script. On a related note, this script will delete your oldest
videos from cloud storage if it needs to, so keep that in mind.

* This script could delete or copy files that it shouldn't, especially if you
set the `LOCAL_VIDEO_DIR` or `ONEDRIVE_VIDEO_DIR` config file parameters
incorrectly. I believe it cannot delete directories, and I think it might not
be able to mess with system files as long as you don't run it with admin
permissions, but it could still theoretically cause lots of trouble! Think
twice about running this script on a computer where you have important files
that are not backed up.

## Notes for JMH

* I wrote this script assuming that we all have lots of local hard drive space.
It seems like that assumption might not hold for most of us (thanks MW 2019).
I think OneDrive has a feature where it will automatically delete local copies
of unused files and keep them in the cloud, but if you need to free up space
immediately, you can right-click on the shared OneDrive folder and select "Free
up space." If this becomes a hassle, let me know, and I can think about
modifying the script to avoid requiring you to run the OneDrive client.

* I have no idea whether this script will actually be worth using over just
manually uploading video files to OneDrive. I hope the benefits outweigh the
downsides, but I had fun just making it, so I won't be offended at all if we'd
rather just share videos manually.

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

## Usage

These usage instructions are also specific to the current version of this
script that uses OneDrive for storage.

1. Record video while playing a game, the way you normally do.

2. After you're done with the game, double-click `upload-videos.py` to run the
script. Look at the text output to see what it's doing. If the script crashes,
copy-paste the output and email it to me.

3. Look at the OneDrive icon in your taskbar and wait for the uploaded videos
to finish syncing. Once they're done syncing, you can go into the shared
OneDrive folder, right-click on video files, and select "Free up space" if you
want to free up space on your local disk.