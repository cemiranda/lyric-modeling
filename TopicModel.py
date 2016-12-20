#Returns true if the year is a leap year after the year 1800
def isleapyear(year):
	if year == 200 or (year % 4 == 0 and year != 1900):
		return(True)
	else: 
		return(False)

#Calculates the days of the week off from the next Saturday 
def daysoff(fulldate, monthdays):
	date = 0
	year = fulldate['year']
	date = fulldate['date']
	month = fulldate['month']
	days = 0
	for value in range(1800, year):
		days = days + 365
		if (isleapyear(value)):
			days = days + 1
	for number in range(1, month):
		days = days + monthdays[number]
	days = days + date - 2
	temp = (((days%7)-3)*-1)
	if(temp<0):
		temp = temp +7
	return(temp)

#Converts the date given to the next Saturday because Billboard's list comes
# out every Saturday
def make_saturday(fulldate, offset, monthdays):
	if(offset == 0):
		return(fulldate)
	fulldate['date'] = fulldate['date'] + offset
	if (fulldate['date']<=monthdays[fulldate['month']]):
		return(fulldate)
	newdate = fulldate['date'] - monthdays[fulldate['month']]
	if(fulldate['month'] == 12):
		fulldate['year'] = fulldate['year'] + 1
		fulldate['month'] = 1
	else :
		fulldate['month'] = fulldate['month'] + 1
	fulldate['date'] = newdate
	return(fulldate)

#Searches through the http code to find the song title given at the index you entered
def getSong(res, whichSong):
	it = re.finditer('chart-row__song', res)
	for match in range(0 ,whichSong):
		x = it.next()
	start = x.end() + 2
	end = start + 100
	string = ''
	for count in range(start, end):
		string = string + res[count]
	found = re.search('</h2', string)
	string = string[0:found.start()]
	return(string.strip())

# Gets the Artist from the HTML code of the website 
def getArtist(res, whichSong):
	it = re.finditer('chart-row__artist', res)
	for match in range(0 ,whichSong):
		x = it.next()
	start = x.end() + 29
	end = start + 100
	string = ''
	for count in range(start, end):
		if(res[count] != ' ' or res[count+1] != ' '):
			string = string + res[count]
	found = re.search('</a', string)
	if(found != None):
	 	string = string[0:found.start()]
	found = re.search('\n', string)
	if(found != None):
	 	string = string[0:found.start()]
	
	found = re.search('/', string)
	while(found !=None):
	 	string = string[found.start()+1:]
	 	found = re.search('/', string)
	return(string.strip())

#Method to make a file with the name string and content a list of the song titles
# and artists 
def makeFile(title, artist, arrayoftitles, lyrics):
	if title in arrayoftitles:
		return
	arrayoftitles.append(title)
	filename = "songs.txt"
	string = (title.title() + '-by-' + artist.title())
	with open(filename, 'a') as file:
		file.write(string + '\n')
	file.close()
	with open(string, 'w') as file:
		file.write(lyrics)
	file.close()

def altertoURL(string):
	replacethis = ["'", ' ', 'amp;', '&-', 'quot;', '?', '&#039;']
	withthis = ['', '-', '', '', '', '', '']
	length = len(replacethis)
	for value in range(0,length):
		index = string.find(replacethis[value])
		while(index != -1):
			string = string.replace(replacethis[value], withthis[value])
			index = string.find(replacethis[value])
	return string

#If the first link fails, it will try additional alterations to the url 
def altertoURL3(string):
	replacethis = ['on-t-', 'an-t-', 'tothe', '.', 'i-ll-', 'i-d-', 'ou-re-',\
					'i-ve-', 'id-nt-', 'at-s-', '--', 'lmo-s-']
	withthis = ['ont-', 'ant-', 'to-the', '', 'ill-', 'id-', 'oure-', 'ive-', 'idnt-', 'ats-','-', 'lmos-'  ]
	length = len(replacethis)
	for value in range(0,length):
		index = string.find(replacethis[value])
		while(index != -1):
			string = string.replace(replacethis[value], withthis[value])
			index = string.find(replacethis[value])
	return string

# Takes the artist of the song and converts it to part of the URL
def altertoURL2(string):
	replacethis = ["'", ' ', 'amp;', 'p!nk', '&-', 'quot;', '...', ',', 'Ne Yo']
	withthis = ['', '-', '', 'pink', '', '', '-', '', 'neyo']
	length = len(replacethis)
	for value in range(0,length):
		index = string.find(replacethis[value])
		if(replacethis[value] == 'amp;'):
			found = re.search('amp;', string)
			if(found != None):
	 			string = string[0:found.start()-2]
		while(index != -1):
			string = string.replace(replacethis[value], withthis[value])
			index = string.find(replacethis[value])
	return string.strip()

# This removes the features and alters the URL to be found more frequently
def removeParenthesisAndFeaturing(string):
	first = re.search('\(', string)
	if(first != None):
		end = re.search('\)', string)
	 	string = string[0:first.start()-1] + string[end.start()+1:]
	first = re.search('Featuring', string)
	if(first != None):
	 	string = string[0:first.start()-1]
	first = re.search('"', string)
	if (first != None):
		string = string[0:first.start()]
	return string.strip()

#This gets the actual lyrics from the metro lyrics URL
def getLyricURL(res, mLength, artist):
	it = re.finditer('lyricbody', res)
	x = it.next()
	start = x.start() + 158
	x = it.next()
	end = x.start()-180
	string = ''
	for count in range(start, end):
		string = string + res[count]
	return (string)

# This removes the HTML code that goes with the Lrics and formats it properly
def formatLyrics(string):
	replacethis = ['<br>',"</p>", '</div>']
	withthis = ['', '', '',]
	length = len(replacethis)
	for value in range(0,length):
		index = string.find(replacethis[value])
		while(index != -1):
			string = string.replace(replacethis[value], withthis[value])
			index = string.find(replacethis[value])
	pattern = '<.*>'
	prog = re.compile(pattern)
	found = re.search(prog, string)
	while(found != None):
		string = string[0:found.start()] + '\n' + string[found.end():]
	 	found = re.search(prog, string)
	pattern = '<.*'
	prog = re.compile(pattern)
	found = re.search(prog, string)
	while(found != None):
		string = string[0:found.start()]
	 	found = re.search(prog, string)

	return string


# Part 2 Methods:
def cleanup(contents, en_stop):
	raw = contents.lower()
	tokens = tokenizer.tokenize(raw)
	try:
		stopped_tokens = [i for i in tokens if not i in en_stop]
	except:
		pass

	return stopped_tokens


# Removes unnecesary lines from lyric files
def removeLine(filename):
	lyrics = ''
	count = 3
   	with open(filename,'r') as f:
        	for line in f:
        	    if (line != '\n' and line != 'language:\n' and line != 'Songwriters\n'):
        	    	if (line == 'meaning\n' or line =='memory\n'):
        	    		count = 0
        	    	elif count < 3 :
        	    		count = count + 1
        	    	else:
            			lyrics = lyrics + line
       	#print filename
       	#print lyrics
   	with open(filename, 'w') as f:
   		f.write(lyrics)

# Removes common words not suitable for topics
def alterLyrics3(replacethis, filename):
	withthis = [' ']
	with open(filename,'r') as f:
         	 lines = f.read()
	length = len(replacethis)
	for value in range(0,length):
		index = lines.find(replacethis[value])
		while(index != -1):
			lines = lines.replace(replacethis[value], withthis[0])
			index = lines.find(replacethis[value])

	return lines

# Returns id in the dictionary of the word given. A little silly method
def wordToId(word, diction):
	return diction[word.strip()]	








#MAIN METHOD
import re
import datetime
import sys
now = datetime.datetime.now()
monthdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


month =1
date=1
year =1959
whichSong = 1
fulldate = {'month': month, 'date' : date, 'year' : year}
currentdate = {'month': month, 'date' : date, 'year' : year}
currentdate['month'] = now.month
currentdate['year'] =  now.year
currentdate['date'] = now.date
#offset2 = daysoff(currentdate, monthdays)
#Ensures the date is the appropriate type if you want to search for a specific date 
if(month< 1 or month>12 or date <0 or date>31 or year<1953 or year>now.year):
	sys.exit("You entered an invlid date!")
if(isleapyear(year)):
	monthdays[2] = 29

offset = daysoff(fulldate, monthdays)
fulldate = make_saturday(fulldate, offset, monthdays)
impossibleURLS = []
arrayoftitles = []
workingURLS = []
boolean = 0
boolean = input("Would you like to download the files now?\nEnter 1 for yes and 0 for no: ")
if(boolean == 1):
	while(True):
		date = fulldate.copy()
		if(date['month']<10):
			date['month'] = ('0' + str(date['month']))
		if(fulldate['date']<10):
			date['date'] = ('0' + str(date['date']))
		billboardurl = ("http://www.billboard.com/charts/hot-100/" + str(date['year']) + "-" + \
		str(date['month']) + "-" + str(date['date']))
		import urllib2
		from urllib2 import Request
		req = Request(billboardurl)
		res = urllib2.urlopen(req).read()
		actualdate = (str(fulldate['month']) + "-" + str(fulldate['date']) +  "-" + str(fulldate['year']))
		#print(billboardurl)
		#print ("Returning the results from date: " + actualdate + '\n')
		title = getSong(res, whichSong)
		artist = getArtist(res, whichSong)
		savedTitle = title
		savedArtist = artist
		if (title == 'Are You Lonesome To-night?' or title =='Stuck On You'):
			artist = 'elvis presley'
		artist = removeParenthesisAndFeaturing(artist)
		title = removeParenthesisAndFeaturing(title)
		title = altertoURL(title.lower())
		artist = altertoURL2(artist.lower())
		#print(title.title() + ' by ' + artist.title())
		metro = ("http://www.metrolyrics.com/" + title + '-lyrics-' + artist + '.html')
		mLength = len(title)
		#print (metro + '\n\n')
		#print('\n\n')
		if (metro not in impossibleURLS):
			try:
				req = Request(metro)
				res = urllib2.urlopen(req).read()
				lyrics = getLyricURL(res, mLength, artist)
				lyrics = formatLyrics(lyrics)
				lyrics = lyrics.strip()
				makeFile(title, artist, arrayoftitles,lyrics)
			except:
				try: #Additional aleration to title if first link fails
					title = altertoURL3(title.lower())
					metro = ("http://www.metrolyrics.com/" + title + '-lyrics-' + artist + '.html')
					req = Request(metro)
					res = urllib2.urlopen(req).read()
					lyrics = getLyricURL(res, mLength, artist)
					lyrics = formatLyrics(lyrics)
					lyrics = lyrics.strip()
					makeFile(title, artist, arrayoftitles,lyrics)
				except:
					#print("There was an error loading " + metro )
					lyrics = ''
					impossibleURLS.append(metro)
					pass
				pass
		if(isleapyear(fulldate['year'])):
			monthdays[2] = 29
		else: 
			monthdays[2] =28
		if(fulldate['date']==monthdays[fulldate['month']]):
			if(fulldate['month']==12):
				fulldate['year']= fulldate['year']+1 
				fulldate['month'] = 1
				fulldate['date'] = 1
			else:
				fulldate['month'] = 1 + fulldate['month']
				fulldate['date'] = 1
		else:
			fulldate['date'] = fulldate['date'] + 1
		fulldate = make_saturday(fulldate, 6, monthdays)
		if(fulldate['date']==28 and fulldate['month']==5 and fulldate['year']==now.year):
			break
		# length = len(impossibleURLS)
		# for value in range (0,length):
		# 	print("This song wasn't found at the URL: " + impossibleURLS[value])

		
with open("songs.txt") as file_obj:
	for line in file_obj:
		lineLength = len(line)
		filename = line[:lineLength-1]
		removeLine(filename)




# Part 2

import sys
import gensim
import re
import lda
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import nltk
from gensim import corpora, models

extra = ["that", " i've ", "can't", "'d", "'ll", "'ve", "'m ", "'re", "don't", ' oooh ', ' ooh ', ' na ', ' oo ', ' babi ', ' oh ', ' danc ', ' just ', "'s ", "'t ", ' know ', ' can ', ' got ']
yesorno = input("Do you want to perform topic modeling on the files? \n Type 1 for yes and 0 for no: ")
word = 'z'
if (yesorno == 0):
	sys.exit()
else:
	pass
while (yesorno == 1):
	en_stop = get_stop_words('en')
	p_stemmer = PorterStemmer()
	tokenizer = RegexpTokenizer(r'\w+')
	texts = []
	with open("songs.txt") as file_obj:
		for line in file_obj:
			lineLength = len(line)
			filename = line[:lineLength-1]
			lines = alterLyrics3(extra, filename)
			#print filename+ '\n'
			#print lines+ '\n\n'
			contents = cleanup(lines, en_stop)
			try:
				stemmed = [p_stemmer.stem(i) for i in contents]
				texts.append(stemmed)
			except:
				pass
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	files = open("wordToID.txt", 'w')
	diction = dictionary.token2id
	files.write(str(diction))  
	files.close()

	tops = input("Enter the number of topics you'd like: ")
	words = input("Enter the number of words per topic: ")
	passes = input("Enter the number of passes you'd like to make: ")
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=tops, id2word = dictionary, passes=passes)
	ldalist = ldamodel.show_topics(num_topics=tops, num_words=words, log=False, formatted=True)
	length = len(ldalist)
	files = open("LDAMODEL.txt", 'r')
	lines = files.read()
	it = re.finditer('Trial', lines)
	count =0
	for match in it:
		count = count + 1
	files.close()
	files = open("LDAMODEL.txt", 'a')
	string = "Trial Number: " + str(count) + "\nNumber of Topics: " + str(tops) + "  Words Per: " + str(words) + "\n"
	files.write(string)
	for value in range(0,length):
		print ldalist[value]
		files.write(str(ldalist[value]) + '\n\n')
	yesorno = input("Would you like to perform another trial? \n Type 1 for yes and 0 for no: ")
	if yesorno == 1:
		word = input('Enter words to exclude for the next round (enter "Done" to stop) also words must be in quotes! ')
		while(word != "Done"):
			extra.append(word)
			word = input('Enter words to not use exclude for the next round (enter "Done" to stop): ')
      
