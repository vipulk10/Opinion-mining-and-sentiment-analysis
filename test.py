#from __future__ import division
import re
import csv
import nltk
import pickle
from pre import processAll
import gettweets
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
		#check if the word stats with an alphabet
		#val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
		#ignore if it is a stop word
		#if(val is None or w in stopWords):
			#continue
		#else:
		featureVector.append(w.lower())
	'''for text in tweet:
            vipul = [word if(word[0:2]=='__') else word.lower() \
                    for word in text.split() \
                    if len(word) >= 3]
            vipul = [stemmer.stem(w) for w in vipul] 
            featureVector.append(vipul)'''
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
		for f in words_uni+words_bi+words_tri:
			bag[f] = 1
		#bag = collections.Counter(words_uni+words_bi+words_tri)

		return bag
featureList = []
#Read the tweets one by one and process it
stopWords = getStopWordList('stopwords.txt')
#start extract_features

def extract_features(tweet):
	############ OLD APPROACH ########################
	'''tweet_words = set(tweet)
	features = {}
	for word in featureList:
		features['contains(%s)' % word] = (word in tweet_words)
	#print features'''
	############# NEW APPROACH #####################################
	features = {}
	word_features = get_word_features(tweet)
	features.update( word_features )
	#if add_negtn_feat :
	negation_features = get_negation_features(tweet)
	#print negation_features
	features.update( negation_features )
 
		#sys.stderr.write( '\rfeatures extracted for ' + str(extract_features.count) + ' tweets' )
	return features
#end

#TO LOAD THE PICKLE CLASSIFIERS..
tweets = []	
inpTweets = csv.reader(open('bigdata.csv', 'rb'), delimiter=',', quotechar='"')
for row in inpTweets:
	sentiment = row[0]
	tweet = row[1]
	processedTweet = processAll(tweet)
	featureVector = getFeatureVector(processedTweet, stopWords)
	#print featureVector
	#featureList.extend(featureVector)
	tweets.append((featureVector, sentiment))
#end loop

data_set = nltk.classify.util.apply_features(extract_features, tweets)
size = int(len(data_set) * 0.15)
training_set, test_set = data_set[size:], data_set[:size]
#print tweets[:size]
print len(test_set)
#from sklearn.svm import LinearSVC
#from nltk.classify.scikitlearn import SklearnClassifier
#NBClassifier = SklearnClassifier(LinearSVC())
#NBClassifier.train(data_set)
NBClassifier = nltk.NaiveBayesClassifier.train(data_set)
#NBClassifier =nltk.classify.decisiontree.DecisionTreeClassifier.train(training_set)
#NBClassifier = nltk.maxent.MaxentClassifier.train(training_set)

#print NBClassifier.classify(extract_features(getFeatureVector(pro,stopWords)))
#print NBClassifier.show_most_informative_features(50)
#print nltk.classify.accuracy(NBClassifier, test_set)*100
#f = open('finalClassifier.pickle','wb')
#pickle.dump(NBClassifier,f)
#f.close()
def loadeverything(searchTerm):
	#featureList =  initialize()
	#f = open('naivebayes_trained_model.pickle')
	#f=open('finalClassifier.pickle')
	#NBClassifier = pickle.load(f)
	#f.close()	
	#print "vipul"
	#Count to check Accuracy:
	count = int(0)
	#accurate = int(0)
	#use tuple
	tweet_set = []
	#remove text file stuff..
	td = gettweets.TwitterData()
	al = td.getData(searchTerm)
	for singletweet in al:
		count = count + 1
		testTweet = singletweet
		processedTestTweet = processAll(testTweet.encode('utf-8'))
		#print extract_features(getFeatureVector(processedTestTweet,stopWords))
		test1 = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet,stopWords)))
		tweet_set.append((count,testTweet,test1))
	#print count
	return tweet_set

#END
'''
y = "tobacco"
x = loadeverything(y)
for i in range(0,len(x)):
	print(x[i][0])
	print(x[i][1]).encode('utf-8')
	print(x[i][2])
	print("\n")
	'''

