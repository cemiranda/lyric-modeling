# lyric-modeling

Lyric Topic Modeling Programs

Programs to get from Billboards top 100 songs, find their respected lyrics, and perform topic modeling on them.

LyricFinder.py:  takes a date and a rank 1-100 and attempts to get the respected song title and artist and then print out the lyrics. Year must be after 1952 because this is the farthest back Billboard has their list. 

TopicModel.py:   creates files with the lyrics of songs found on Billboard top 100 from 1959 to current day. Then performs topic modeling on the lyrics collected. It allows you to input words you would like to remove with each pass. Downloading of the songs takes up to 20 minutes depending on internet speed, therefore I included a zipped file of the songs it collects if you don't wish to wait. If you'd like to use the zip file, make sure the program is in the same directory as the song files.

