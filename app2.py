import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

data_processing = pd.read_csv('data.csv', encoding='ISO-8859-1')
data_processing.head()

data_processing.mean(numeric_only=True)

data_processing.median()

data_processing.count(numeric_only=True)

data_processing.describe()

data_processing['total_char'] = data_processing['Tweet'].apply(len)
data_processing.head()

def split_sentence(s):
    return len(s.split())

data_processing['total_word'] =  data_processing['Tweet'].apply(split_sentence)
data_processing.head()

data_processing.var()

data_processing.std()

data_processing.skew()

data_processing.kurtosis()

data_processing.corr()

# from wordcloud import WordCloud
# Tweet = ' '.join(data_processing['Tweet'])
# wordcloud = WordCloud().generate(Tweet)

# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()

data_processing.plot(x='total_word', y='total_char', kind='scatter')

data_processing.tail(25)

data_processing.shape

data_processing.info()

data_processing.describe()

data_processing.isnull().sum()

from unidecode import unidecode

def replace_ascii(s):
    return unidecode(s)

def remove_ascii2(s):
    newText = re.sub(r'\\x[A-Za-z0-9./]+',' ', unidecode(s))
    return newText

data_processing['CleanedTweet'] = data_processing['Tweet'].apply(remove_ascii2)
data_processing.head()

def removeBytesText(s):
    newText = re.sub(r'\\x.{2}',' ', s)
    return newText

data_processing['CleanedTweet1'] = data_processing['CleanedTweet'].apply(removeBytesText)
data_processing.head()

data_processing.drop(data_processing.columns[15], axis=1, inplace=True)
data_processing.head()

def removeNewLine(s):
    newText = re.sub(r'\n',' ', s)
    return newText

data_processing['CleanedTweet2'] = data_processing['CleanedTweet1'].apply(removeNewLine)
data_processing.tail()

data_processing.drop(data_processing.columns[15], axis=1, inplace=True)
data_processing.head()

def removeNewLineText(s):
    newText = re.sub(r'\\n.{0}',' ', s)
    return newText

data_processing['CleanedTweet3'] = data_processing['CleanedTweet2'].apply(removeNewLineText)
data_processing.head()

data_processing.drop(data_processing.columns[15], axis=1, inplace=True)
data_processing.head()

def removePunc(s):
    newText = re.sub(r'[^\w\s]',' ',s)
    return newText

data_processing['CleanedTweet4'] = data_processing['CleanedTweet3'].apply(removePunc)
data_processing.head()

data_processing.drop(data_processing.columns[15], axis=1, inplace=True)
data_processing.head()

def removeMoreSpace(s):
    newText = re.sub('  +', '', s)
    return newText

data_processing['CleanedTweet'] = data_processing['CleanedTweet4'].apply(removeMoreSpace)
data_processing.head()

data_processing.drop(data_processing.columns[15], axis=1, inplace=True)
data_processing.head()

data_processing.describe()

data_processing.shape

len(data_processing['Tweet'][0])

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.drop(data_processing.columns[1], axis=1, inplace=True)
data_processing.head()

data_processing.corr()

data_processing.total_char.hist()

data_processing.total_word.hist()

data_processing.describe()

conn = sqlite3.connect('datas/challenge.db')
sql = 'SELECT * FROM challange_data;'
data_processing_challenge_db = pd.read_sql(sql, conn)
conn.close()
data_processing_challenge_db

#menggabungkan semua text dalam dataframe, menjadi satu string
# CleanedTweet = ' '.join(data_processing_challenge_db['CleanedTweet']) 
# wordcloud = WordCloud().generate(CleanedTweet)

# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()

def clasify_label(hs):
    label = ''
    if int(hs) == 1:
        label = 'positive'
    else:
        label = 'negative'
    return label

data_processing_challenge_db['hs_label'] = data_processing_challenge_db['HS'].apply(clasify_label)
data_processing_challenge_db.head()

plt.figure(figsize=(12,6))
sns.countplot(x='hs_label', data=data_processing_challenge_db)

corr = data_processing_challenge_db.corr()
sns.heatmap(corr)

sns.distplot(data_processing_challenge_db.total_word)