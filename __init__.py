from __future__ import division
from flask import Flask, render_template, request
import re
import test
app = Flask(__name__)


#FOR API:
@app.route('/q=<searchterm>')
def api_printing(searchterm):
	searchterm = re.sub(' ','&',searchterm)
	all_tweets = test.loadeverything(searchterm)
	number_pos = int(0)
	number_neg = int(0)
	number_neut = int(0)
	count = int(0)
	for a in all_tweets:
		if(a[2] == 'positive'):
			number_pos = number_pos + 1
			count = count + 1
		elif(a[2] == 'neutral'):
			number_neut = number_neut +1
			count = count + 1
		elif(a[2] == 'negative'):
			number_neg = number_neg + 1
			count = count + 1
	npos = (number_pos/count)*100
	nneg = (number_neg/count)*100
	nneut = (number_neut/count)*100
	return render_template("api.html", search_term=searchterm, all_tweets=all_tweets,\
	pos = npos, neg = nneg, neut = nneut)

@app.route('/')

def homepage():
	ask_graph = "false"
	return render_template("index.html", ask_graph = ask_graph)

@app.route('/', methods=['POST'])
def throw_graph():
	ask_graph = "true"
	text = request.form['text']
	#x = test2.poop()
	text = re.sub('[\s]','&',text)
	all_tweets = test.loadeverything(text)
	number_pos = int(0)
	number_neg = int(0)
	number_neut = int(0)
	count = int(0)
	for a in all_tweets:
		if(a[2] == 'positive'):
			number_pos = number_pos + 1
			count = count + 1
		elif(a[2] == 'neutral'):
			number_neut = number_neut +1
			count = count + 1
		elif(a[2] == 'negative'):
			number_neg = number_neg + 1
			count = count + 1
	npos = (number_pos/count)*100
	nneg = (number_neg/count)*100
	nneut = (number_neut/count)*100
	return render_template("index.html", ask_graph = ask_graph,\
	 text = text, pos = npos, neg = nneg, neut = nneut, all_tweets = all_tweets)


if __name__ == "__main__":
	app.debug = True
	app.run()