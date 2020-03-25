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
