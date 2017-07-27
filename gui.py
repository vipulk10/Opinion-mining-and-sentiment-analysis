import re
import csv
import nltk
import pickle
from pre import processAll
#initialize stopWords
stopWords = []
#start replaceTwoOrMore
def replaceTwoOrMore(s):
	#look for 2 or more repetitions of character and replace with the character itself
	pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
	#read the stopwords file and build a list
	stopWords = []
	#stopWords.append('AT_USER')
	#stopWords.append('URL')

	fp = open(stopWordListFileName, 'r')
	line = fp.readline()
	while line:
		word = line.strip()
		stopWords.append(word)
		line = fp.readline()
	fp.close()
	return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
	featureVector = []
	
	#split tweet into words
	words = tweet.split()
	for w in words:
		#replace two or more with two occurrences
		w = replaceTwoOrMore(w)
		#strip punctuation
		w = w.strip('\'"?,.')
		
		featureVector.append(w.lower())
	
	return featureVector
#end

#http://www.clips.ua.ac.be/NeSpNLP2010/nespnlp2010-proceedings.pdf
#https://github.com/yogeshg/Twitter-Sentiment
negtn_regex = re.compile( r"""(?:
		^(?:never|no|nothing|nowhere|noone|none|not|
			havent|hasnt|hadnt|cant|couldnt|shouldnt|
			wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
		)$
	)
	|
	n't
	""", re.X)
def get_negation_features(words):
		INF = 0.0
		negtn = [ bool(negtn_regex.search(w)) for w in words ]
	
		left = [0.0] * len(words)
		prev = 0.0
		for i in range(0,len(words)):
			if( negtn[i] ):
				prev = 1.0
			left[i] = prev
			prev = max( 0.0, prev-0.1)
	
		right = [0.0] * len(words)
		prev = 0.0
		for i in reversed(range(0,len(words))):
			if( negtn[i] ):
				prev = 1.0
			right[i] = prev
			prev = max( 0.0, prev-0.1)
	
		return dict( zip(
						['neg_l('+w+')' for w in  words] + ['neg_r('+w+')' for w in  words],
						left + right ) )
	

def get_word_features(words):
		bag = {}
		#####  https://docs.python.org/2/tutorial/datastructures.html
		words_uni = [ 'has(%s)'% ug for ug in words ]
		#wwords_uni = list(set(words_uni))
		words_bi  = [ 'has(%s)'% ','.join(map(str,bg)) for bg in nltk.bigrams(words) ]
		words_tri = [ 'has(%s)'% ','.join(map(str,tg)) for tg in nltk.trigrams(words) ]
		for f in words_uni:#+words_bi+words_tri:
			bag[f] = 1
		return bag
featureList = []
#Read the tweets one by one and process it
stopWords = getStopWordList('stopwords.txt')
#start extract_features

def extract_features(tweet):
	
	############# NEW APPROACH #####################################
	features = {}
	word_features = get_word_features(tweet)
	features.update( word_features )
	#if add_negtn_feat :
	negation_features = get_negation_features(tweet)
	#print negation_features
	features.update( negation_features )
	return features
#end

#TO LOAD THE PICKLE CLASSIFIERS..
tweets = []	
inpTweets = csv.reader(open('full_training_dataset.csv', 'rb'), delimiter=',', quotechar='"')
for row in inpTweets:
	sentiment = row[0]
	tweet = row[1]
	processedTweet = processAll(tweet)
	featureVector = getFeatureVector(processedTweet, stopWords)
	tweets.append((featureVector, sentiment))
#end loop

data_set = nltk.classify.util.apply_features(extract_features, tweets)
NBClassifier = nltk.NaiveBayesClassifier.train(data_set)
def loadeverything(searchTerm):
	#al = ["i am sorry sorry"]
		testTweet = searchTerm
		processedTestTweet = processAll(testTweet.encode('utf-8'))
		#print extract_features(getFeatureVector(processedTestTweet,stopWords))
		test1 = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet,stopWords)))
		return test1
from Tkinter import *

def show_message():
	whatever_you_do = show_entry_fields()
	msg = Message(master, text = whatever_you_do)
	msg.config(bg='lightgreen', font=('times', 24, 'italic'))
	msg.pack( )
def show_entry_fields():
   print("sentiment of the text is: %s\n" % (loadeverything(e1.get())))
   #return loadeverything(e1.get())

master = Tk()
Label(master, text="Text").grid(row=0)
#Label(master, text="Last Name").grid(row=1)

e1 = Entry(master)
#e2 = Entry(master)

e1.grid(row=0, column=1)
#e2.grid(row=1, column=1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )