import pandas as pd
import matplotlib.pyplot as plt
import copy
from datetime import timedelta
from collections import Counter
import nltk

# 1. Measuring firm performance
# Readi1ng the csv file into a data frame
df = pd.read_csv("input.csv")

# Creating key for join
df['combo_key'] = df['gvkey'].map(str) + df['fyearq'].map(str) + df['fqtr'].map(str)
df['d_netincome'] = df['niq'] > 0
df['d_operating'] = df['oancfy'] > 0
df['d_quality'] = df['oancfy'] > df['niq'] 
df['longterm'] = df['dlttq']/df['atq']
df['current'] =  df['actq']/df['lctq']
df['gross_margin'] = (df['revtq'] - df['cogsy'])/df['revtq']
df['asset_turn'] = df['revtq']/df['atq']
df['roa'] = df['niq']/df['atq']
df['market_cap'] = df['cshoq']*df['prccq']
df['btm'] = df['ceqq']/df['market_cap']

#For quarterly variables
df_ref = copy.copy(df)
df_ref['new_year'] = df_ref['fyearq']+1
df_ref['combo_key'] = df_ref['gvkey'].map(str) + df_ref['new_year'].map(str) + df_ref['fqtr'].map(str)
df_merged = pd.merge(df_ref, df, how='inner', on ='combo_key')

# x - past year; y - current year
#F-Score variables

df_merged['d_roa'] = df_merged['roa_y'] > df_merged['roa_x']
df_merged['d_longterm'] = df_merged['longterm_y'] < df_merged['longterm_x']
df_merged['d_currentro'] = df_merged['current_y'] > df_merged['current_x']
df_merged['d_shareout'] = df_merged['cshoq_y'] <= df_merged['cshoq_x']
df_merged['d_gm'] = df_merged['gross_margin_y'] > df_merged['gross_margin_x']
df_merged['d_at'] = df_merged['asset_turn_y'] > df_merged['asset_turn_x']
df_merged['fscore'] = df_merged[['d_netincome_y', 'd_operating_y', 'd_quality_y', 'd_roa', 'd_longterm', 'd_currentro', 'd_shareout', 'd_gm','d_at']].sum(axis=1)

results = df_merged[['d_roa', 'd_longterm', 'd_currentro', 'd_shareout', 'd_gm','d_at','fscore']].mean().reset_index()
print (df_merged[['d_roa', 'd_longterm', 'd_currentro', 'd_shareout', 'd_gm','d_at','fscore']].mean())

plt.hist(df_merged['fscore'])

total =  df['gvkey'].size
f7 = df_merged[df_merged['fscore']>=7]['gvkey_y'].size
print '1.a) % of overall sample with F-Score >= 7 is {:.2f}%'.format(float(f7)*100/total)

print'Median of Book to Market ratio is {:.5f}'.format(df_merged['btm_y'].median())

for key in df_merged.groupby(['fyearq_y']):
    df_merged['decile'] = pd.qcut(df_merged['btm_y'],5,labels = False)

f7d5 = df_merged[(df_merged['fscore']>=7) & (df_merged['decile']==4)]['gvkey_x'].size
print '% of overall sample with F-Score >= 7 and with top quantile Book to Market Ratio is {:.2f}%'.format(float(f7d5)*100/total)

#average F-score for each quintile of BTM 
print df_merged.groupby('decile')['fscore'].mean()

# 2.  Timing of Information Flows – is it random?
df_merged['date'] = pd.to_datetime(df_merged['rdq_y'], format='%d%b%Y') 
df_merged['data_date'] = pd.to_datetime(df_merged['datadate_y'], format='%d%b%Y')
df_merged['delay']= df_merged['date'] - df_merged['data_date']
df_merged['delay_days']= (df_merged['delay'].map(timedelta.total_seconds))//(3600*24)

# Excluding negative values of date and winsorizing the data
df_merged['delay_days'] = df_merged.delay_days.map(lambda x: 0 if x<0 else x)
df_merged['delay_days'] = df_merged.delay_days.map(lambda x: 121 if x>120 else x)

# Grouped by quarter
print df_merged.groupby('fqtr_y').delay_days.mean()

print 'Pearson correlation between delay and the Piotroski F-score is {:.2f} '.format(df_merged.delay_days.corr(df_merged.fscore))

# 3. Bag of words 
tokenizer = nltk.RegexpTokenizer(r'\w+')
tesla, pos, neg = [],[],[]
with open('HW7_Tesla_2015.txt','r') as text:
    raw = text.read()
    tesla = tokenizer.tokenize(raw)
    tesla = [x.strip().lower() for x in tesla]
    print 'There are {} words in the Tesla text'.format(len(tesla))

tesla_dict = dict(pd.Series(tesla).value_counts())
pos_words = pd.read_csv('HW7_LM_pos_words.txt', squeeze = True).tolist()
neg_words = pd.read_csv('HW7_LM_neg_words.txt', squeeze = True).tolist()
pos_words = [x.strip().lower() for x in pos_words]
neg_words = [x.strip().lower() for x in neg_words]

count_pos, count_neg = 0,0
count = 0
for k,v in tesla_dict.items():
    if k.strip().lower() in pos_words:
        print k,v
        count_pos += v
        
for k,v in tesla_dict.items():
    if k.strip().lower() in neg_words:
        print k,v
        count_neg += v    
    
print 'Sentiment Analysis'
print 'a. {:.2f}%'.format(float(count_pos-count_neg))*100/len(tesla))
print '2. {:.2f}%'.format(float(count_neg)*100/len(tesla))
print 'Number of negator(no) words is {}'.format(sum('no' == word for word in tesla))
print 'Number of negator(not) words is {}'.format(sum('not' == word for word in tesla))
print 'Number of negator(never) words is {}'.format(sum('never' == word for word in tesla))
