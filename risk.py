import pandas as pd
import nltk

# Expedia risk.txt
def lm_sentiment_risk(file):
  tokenizer = nltk.RegexpTokenizer(r'\w+')
  risk = []
  with open(file,'r') as text:
      raw = text.read()
      risk = tokenizer.tokenize(raw)
      risk = [x.strip().lower() for x in risk]
      print 'There are {} words in the Expedia text'.format(len(risk))
  
  risk_dict = dict(pd.Series(risk).value_counts())
  pos_words = pd.read_csv('LM_pos_words.txt', squeeze = True).tolist()
  neg_words = pd.read_csv('LM_neg_words.txt', squeeze = True).tolist()
  pos_words = [x.strip().lower() for x in pos_words]
  neg_words = [x.strip().lower() for x in neg_words]
  
  count_pos, count_neg = 0,0
  for k,v in risk_dict.items():
      if k.strip().lower() in pos_words:
          count_pos += v
          
  for k,v in risk_dict.items():
      if k.strip().lower() in neg_words:
          count_neg += v    
      
  print 'Sentiment Analysis'
  print 'a. {:.2f}%'.format(float(count_pos-count_neg)*100/len(risk))
  print '2. {:.2f}%'.format(float(count_neg)*100/len(risk))
  print 'Number of negator(no) words is {}'.format(sum('no' == word for word in risk))
  print 'Number of negator(not) words is {}'.format(sum('not' == word for word in risk))
  print 'Number of negator(never) words is {}'.format(sum('never' == word for word in risk))

lm_sentiment_risk('expedia_management_2016.txt')
lm_sentiment_risk('expedia risk 2015.txt')
lm_sentiment_risk('expedia risk 2014.txt')
