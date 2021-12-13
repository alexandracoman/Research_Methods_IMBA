import collections
import csv
import sys
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import re
import string
import nltk
from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
# nltk.download('punkt')


def get_domains_list_and_number(data_frame):

    domains_list = data_frame['domain'].unique()
    domains_number = data_frame.nunique()['domain']

    return domains_list, domains_number

def get_types_lsit_and_number(data_frame):
    types_list = data_frame['type'].unique()
    types_number = data_frame.nunique()['type']

    return types_list, types_number

def get_authors_lsit_and_number(data_frame):
    authors_list = data_frame['authors'].unique()
    authors_number = data_frame.nunique()['authors']

    return authors_list, authors_number


def create_word_cloud(str_list, file_name):
    s = str(str_list)

    wordcloud = WordCloud(width = 500, height = 500, background_color = 'white', min_font_size=1).generate(s)
    
    wordcloud.to_file(file_name)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
def create_horizontal_domains_chart(df):
    tmp_list = []
    d_list = []
    c_list = []
    
    for row in df.groupby('domain').count().iterrows():
        tmp_list.append((row[0], row[1]['type']))
    
    tmp_list_sort = sorted(tmp_list, key=lambda x: x[1], reverse=True)
    
    d_list = [e[0] for e in tmp_list_sort]
    c_list = [e[1] for e in tmp_list_sort]

    d_list = d_list[0:50]
    c_list = c_list[0:50]

    plt.rcParams["figure.figsize"] = (20,10)
    plt.barh(d_list, c_list)
    plt.title('Most frequent fake news web domains')
    plt.ylabel('Domain')
    plt.xlabel('Frequency')
    plt.savefig('domains_bar_chart.png')

def process_titles(df):
    all_words = []
    cnt = 0
    for row in df.iterrows():
        clean_data = str(row[1]['title'])
        
        # Remove numbers
        clean_data = re.sub(r'\d+', '', clean_data).lower()
        
        # Remove https urls
        clean_data = re.sub(r'https?:\/\/.*[\r\n]*', '',clean_data, flags=re.MULTILINE)
        
        # Remove www urls
        clean_data = re.sub(r'www.*.*', '', clean_data)

        # Remove email addresses
        clean_data = re.sub(r'\S*@\S+', '', clean_data)

        # Remove punctuation
        clean_data = clean_data.translate(str.maketrans('', '', string.punctuation)).strip()

        # Remove \n
        clean_data = re.sub(r'\n+', ' ', clean_data)

        # Remove multiple spaces
        clean_data = re.sub(r' +', ' ', clean_data)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        row_tokens = word_tokenize(clean_data)

        # Clean words from non letter chars
        row_tokens = [re.sub(r'[^a-z]+', '', w) for w in row_tokens]
        filtered_tokens = [w for w in row_tokens if w not in stop_words and len(w) > 3]

        # Append current title word list to final word list
        all_words.extend(filtered_tokens)
        cnt += 1
        print(cnt)
    
    counted_words = collections.Counter(all_words)
    words_df = pd.DataFrame(counted_words.most_common(45), columns=['Word', 'Frequency'])
    print(words_df.head())

    w_list = [e[0] for e in counted_words.most_common(45)]
    c_list = [e[1] for e in counted_words.most_common(45)]

    plt.rcParams["figure.figsize"] = (18,10)
    plt.barh(w_list, c_list)
    plt.title('Most frequent words in fake news titles')
    plt.ylabel('Word')
    plt.xlabel('Frequency')
    plt.savefig('word_bar_chart.png')

def create_horizontal_type_chart(df):
    tmp_list = []
    t_list = []
    c_list = []
    
    for row in df.groupby('type').count().iterrows():
        tmp_list.append((row[0], row[1]['domain']))

    t_list = [e[0] for e in tmp_list]
    c_list = [e[1] for e in tmp_list]

    plt.rcParams["figure.figsize"] = (10,10)
    plt.bar(t_list, c_list)
    plt.title('Most frequent fake news types')
    plt.xticks(rotation=45)
    plt.xlabel('Type')
    plt.ylabel('Frequency')
    plt.savefig('types_bar_chart.png')    

if __name__ == "__main__" :

    df = pd.read_csv(sys.argv[1], dtype='unicode')

    # d_list, d_number = get_domains_list_and_number(df)

    # t_list, t_number = get_types_lsit_and_number(df)

    # a_list, a_number  = get_authors_lsit_and_number(df)

    # Create web domains word cloud 
    # create_word_cloud(d_list, 'domains.png')

    # Crate take news types word cloud
    # create_word_cloud(t_list, 'types.png')

    # Create domains chart
    create_horizontal_domains_chart(df)

    # Create types chart
    # create_horizontal_type_chart(df)

    # Get word frequency in titles
    # process_titles(df)
