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
#def getArtist(res, whichSong):
#	it = re.finditer('chart-row__artist', res)
#	for match in range(0 ,whichSong):
#		x = it.next()
#	start = x.end()+50
#	end = start + 150
#	string = ''
#	for count in range(start, end):
#		if(res[count] != ' ' or res[count+1] != ' '):
#			string = string + res[count]
#	found = re.search('>', string)
#	if(found != None):
#	 	string = string[found.start()+1:]
#	string = string.strip()
#	found = re.search('</a', string)
#	if(found != None):
#	 	string = string[0:found.start()]
#	found = re.search('\n', string)
#	if(found != None):
#	 	string = string[0:found.start()]
	#found = re.search('/', string)
	#while(found !=None):
	 #	string = string[found.start()+1:]
	 #	found = re.search('/', string)
	#return(string.strip())

# Takes the title name and converts it to part of the URL 
def altertoURL(string):
	replacethis = ["'", ' ', 'amp;', '&-', 'quot;', '?', '&#039;', 'on-t-', 'an-t-', 'tothe', 'ne-yo', '.', 'i-ll-', 'i-d-', 'ou-re-',\
					'i-ve-', 'id-nt-', 'at-s-', '--', 'lmo-s-']
	withthis = ['', '-', '', '', '', '', '', 'ont-', 'ant-', 'to-the', 'neyo', '', 'ill-', 'id-', 'oure-', 'ive-', 'idnt-', 'ats-','-', 'lmos-'  ]
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

#MAIN METHOD
import re
import datetime
import sys
import urllib2
from urllib2 import Request

print("Welcome!")
now = datetime.datetime.now()
monthdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month = input("Please enter the month of the song lyrics you'd like to get:  ")
date = input("Please enter the date of the song lyrics you'd like to get:  ")
year = input("Please enter the year of the song lyrics you'd like to get:  ")
whichSong = input("Enter the rank of the song on this billboard you'd like the lyrics to: ")
offset = 0
fulldate = {'month': month, 'date' : date, 'year' : year}

if(month< 1 or month>12 or date <0 or date>31 or year<1953 or year>now.year):
	sys.exit("You entered an invlid date!")

if(isleapyear(year)):
	monthdays[2] = 29

offset = daysoff(fulldate, monthdays)
fulldate = make_saturday(fulldate, offset, monthdays)

if(fulldate['month']<10):
	fulldate['month'] = ('0' + str(fulldate['month']))
if(fulldate['date']<10):
	fulldate['date'] = ('0' + str(fulldate['date']))

billboardurl = ("http://www.billboard.com/charts/hot-100/" + str(fulldate['year']) + "-" + \
	 str(fulldate['month']) + "-" + str(fulldate['date']))


req = Request(billboardurl)
res = urllib2.urlopen(req).read()
actualdate = (str(fulldate['month']) + "-" + str(fulldate['date']) + "-" + str(fulldate['year']))
print ("Returning the results from date: " + actualdate+'\n')
title = getSong(res, whichSong)
artist = getArtist(res, whichSong)
artist = removeParenthesisAndFeaturing(artist)
title = removeParenthesisAndFeaturing(title)
title = altertoURL(title.lower())
artist = altertoURL2(artist.lower())
print(title.title() + ' by ' + artist.title())
metro = ("http://www.metrolyrics.com/" + title + '-lyrics-' + artist + '.html')
mLength = len(title)
try:
	req = Request(metro)
	res = urllib2.urlopen(req).read()
	lyrics = getLyricURL(res, mLength, artist)
	lyrics = formatLyrics(lyrics)		
	print lyrics
except:
	print("There was an error loading lyrics for song at: " + metro )
	lyrics = ''
	pass
