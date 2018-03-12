import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# atq - total assets, revtq - total revenue 
df = pd.read_csv("EXPE Balance Sheet.csv")
df['f2016'] = abs(df['2016']*100).astype('str').str[0].astype('int')
df['f2015'] = abs(df['2015']*100).astype('str').str[0].astype('int')
df['f2014'] = abs(df['2014']*100).astype('str').str[0].astype('int')
plt.hist(df['f2016'].value_counts())
plt.hist(df['f2015'].value_counts())
plt.hist(df['f2014'].value_counts().transpose())
df_x = df['f2016'].value_counts().to_frame(name ='Count')
print df_x
df_x = df_x[df_x['Count'].index>0].sort_index()
df_x['Number'] = df_x['Count'].index
df_x['Expected'] = np.log10(1 + (1/df_x['Number']))
df_x['Cuml_Exp'] = df_x['Expected'].cumsum()*100
df_x['Actual'] = df_x['Count']/df_x['Count'].sum()
df_x['Cuml_Act'] = df_x['Actual'].cumsum()*100
df_x['Cuml Diff'] = abs(df_x['Actual'] - df_x['Expected'])
print 'Cutoff statistic for x is {:.2f}%'.format(1.36/np.sqrt(df_x['Count'].sum()))
print 'Calculated KS statistic for x is {:.2f}%'.format(df_x['Cuml Diff'].max()) 

df_y = df['f2015'].value_counts().to_frame(name ='Count')
print df_y
df_y = df_y[df_y['Count'].index>0].sort_index()
df_y['Number'] = df_y['Count'].index
df_y['Expected'] = np.log10(1 + (1/df_y['Number']))
df_y['Cuml_Exp'] = df_y['Expected'].cumsum()*100
df_y['Actual'] = df_y['Count']/df_y['Count'].sum()
df_y['Cuml_Act'] = df_y['Actual'].cumsum()*100
df_y['Cuml Diff'] = abs(df_y['Actual'] - df_y['Expected'])
print 'Cutoff statistic for y is {:.2f}%'.format(1.36/np.sqrt(df_y['Count'].sum()))
print 'Calculated KS statistic for y is {:.2f}%'.format(df_y['Cuml Diff'].max()) 

df_z = df['f2014'].value_counts().to_frame(name ='Count')
print df_z
df_z = df_z[df_z['Count'].index>0].sort_index()
df_z['Number'] = df_z['Count'].index
df_z['Expected'] = np.log10(1 + (1/df_z['Number']))
df_z['Cuml_Exp'] = df_z['Expected'].cumsum()*100
df_z['Actual'] = df_z['Count']/df_z['Count'].sum()
df_z['Cuml_Act'] = df_z['Actual'].cumsum()*100
df_z['Cuml Diff'] = abs(df_z['Actual'] - df_z['Expected'])
print 'Cutoff statistic for z is {:.2f}%'.format(1.36/np.sqrt(df_z['Count'].sum()))
print 'Calculated KS statistic for z is {:.2f}%'.format(df_z['Cuml Diff'].max()) 