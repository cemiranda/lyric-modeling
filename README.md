# lyric-modeling

Lyric Topic Modeling Programs

Programs to get from Billboards top 100 songs, find their respected lyrics, and perform topic modeling on them.

LyricFinder.py: takes a date and a rank 1-100 and attempts to get the respected song title and artist and then print out the lyrics from metrolyrics.com. Year must be after 1959 because this is the farthest back Billboard has their list. 

TopicModel.py:  creates files with the lyrics of songs found on Billboard top 100 from 1959 to current day. Then performs topic modeling on the lyrics collected. The download of songs takes about 20 minutes therefore I would recommend using the already downloaded files in the LyricModel.zip.


I would recommend downloading the LyricModel.zip file. This has the setup already configured. The files LyricFinder.py and TopicModel.py would be found in the Songs directory. You should be able to run the programs directly from that folder without difficulty.

Requirements: Must have lda, gensim, stop-words and nltk installed. Use "sudo easy_install -U _____" to install packages. 
