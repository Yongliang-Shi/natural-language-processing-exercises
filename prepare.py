import pandas as pd

import unicodedata
import re

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

# %%
def basic_clean(original):
    '''
    The function takes in a string and does the basic clean to the string
    '''
    
    # convert text to all lower case for normalcy. 
    article = original.lower()
    
    # remove any accented, non-ACSII cahracters 
    article = unicodedata.normalize('NFKD', article)\
                .encode('ascii', 'ignore')\
                .decode('utf-8', 'ignore')
    
    # replace anthing that is not a letter, number, whitespace 
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    
    return article                

# %%
def tokenize(original):
    '''
    This function takes in a string and returns a tokenized string. 
    '''
    # Create the object
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use the tokenizer
    article = tokenizer.tokenize(original, return_str=True)
    
    return article

# %%
def stem(article):
    '''
    This function takes in a string and returns a string with words stemmed. 
    '''    
    # Create the nltk stemmer object
    ps = nltk.porter.PorterStemmer()
    
    # Use list comprehension to stemmingly transform all the words in the article
    stems = [ps.stem(word) for word in article.split()]
    
    # Join the stemmed words back to a string
    stemmed_article = ' '.join(stems)
    
    return stemmed_article

# %%
def lemmatize(article):
    '''
    This function takes in a string and returns a string with words lemmatized. 
    '''
    
    # Create the nltk lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use list comprehension to lemmatizedly transform all the words in the article
    lemmas = [wnl.lemmatize(word) for word in article.split()]
    
    # Join the lemmatized words back to a string
    lemmatized_article = ' '.join(lemmas)
    
    return lemmatized_article

# %%
def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    This function takes in a string, optional extra_words and exlude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in the text
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list
    stopword_list = stopword_list.union(set(extra_words))
    
    # Split words in the string
    words = string.split()
    
    # Create a list of words from the string with stopwords removed and assign to variable
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a varibale
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

# %%
def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with the option
    to pass lists for extra_words and exlucde_words and returns a df with the text article title, 
    original text, stemmed text, lemmatized text, cleaned-tokenized-lemmatized-stopwords removed text.  
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words)\
                            .apply(lemmatize)
    
    df['stemmed'] = df[column].apply(basic_clean).apply(stem)
    
    df['lemmatized'] = df[column].apply(basic_clean).apply(lemmatize)
    
    return df[['title', column, 'stemmed', 'lemmatized', 'clean']]