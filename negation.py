import re
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
		negtn = [ bool(negtn_regex.search(w)) for w in words]
	
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
		print left
		print right
		print left+right
		print zip(left,right)
		print (['neg_l('+w+')' for w in  words],left)
		print (['neg_r('+w+')' for w in  words],right)
		print dict( zip(
						['neg_l('+w+')' for w in  words] + ['neg_r('+w+')' for w in  words],
						left + right ) )
vipul=['this', 'aint', 'good']
get_negation_features(vipul)
	