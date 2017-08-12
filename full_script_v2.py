# -*- coding: utf-8 -*-

import glob, os, io, re
import pandas as pd
import textminer as tm
import matplotlib.pyplot as plt
import quickndirty as qd

wd = os.getcwd()
filepath = os.path.join(wd,'letters_text\\')
filenames = glob.glob(filepath + '*.txt')

os.chdir(filepath)

def read_txt_lines(filepath):
    with io.open(filepath, 'r', encoding = 'utf-8') as f:
        content = f.readlines()
    return content

content_list = []
for filename in filenames:#loop over filenames
    text = read_txt_lines(filename)# read file
    content_list.append(text)# add file to result list

text = []
metadata = []
letters_text = []
letters_metadata = []
for letter in content_list:
    text = letter[:-4]
    letters_text.append(text)
    metadata = letter[-4:]
    letters_metadata.append(metadata)

#### ISOLATE DATE, SENDER, RECIPIENT
#we join the previous list together, so we have a string for each letter's metadata
metadata_unified = []
metadata_unified_list = []

for letter in letters_metadata:
     metadata_unified = ''.join(letter)
     metadata_unified_list.append(metadata_unified)

#alright lets get these lists of date, author and recipient
index = 0
match_date = ''
letters_dates = []
match_author = ''
letters_author = []
match_recipient = ''
letters_recipient = []
for letter in metadata_unified_list:
    match_date = re.compile(r"\d{4}.*[)]").search(letter) #search each letter for this pattern
    
    if match_date is not None: #if there is a match append the string minus the parenthesis 
        letters_dates.append(match_date.group()[:-1])
    else: #if there is no match insert 'nodate' into the list
        letters_dates.insert(index,'0') ###THIS DOESNT WORK!!!!!!!!!!!!!!!
        
    match_author = re.compile(r"FRA:(.*?)\d{4}").search(letter)
    if match_author is not None:
        letters_author.append(match_author.group()[5:-6]) #THIS DOESNT WORK WELL EITHER
    else:
        letters_author.insert(index,'noauthor')
        
    match_recipient = re.compile(r"BREV TIL:(.*)FRA:").search(letter) 
    if match_recipient is not None:
        letters_recipient.append(match_recipient.group()[10:-5])
    else:
        letters_recipient.insert(index,'norecipient')
    
    index = index + 1

### GET THE YEARS

year = ''
mean_list = []
letters_years = []
for text in letters_dates:
        year = text[:4]
        letters_years.append(year)

### REMOVE METADATA FROM TEXT STRING
letters_text_strings = []
string = ''
for text in letters_text:
    string = ''.join(text)
    letters_text_strings.append(string)
print(letters_text_strings[0])

letters_metadata_strings = []
string = ''
for text in letters_metadata:
    string = ''.join(text)
    letters_metadata_strings.append(string)
print(letters_metadata_strings[0])

cleaner = ''
metd = ''
index = 0
letters_text_clean = []
for text in letters_text_strings:
    metd = letters_metadata_strings[index]
    cleaner = text.replace(metd,'')
    letters_text_clean.append(cleaner)
    index = index + 1

print(letters_text_clean[:2])


### TOKENIZE THE STUFF
def tokenize_text(string, lentoken = 0): # 0 is the default value for the var lentoken
    """
    Function splits string into tokens by everything that is not a letter. æ-ø-å does not count as a letter.
    """
    tokenizer = re.compile(r'[^a-zA-ZæøåÆØÅöüÖÜ]') #python 3 version - her er æ-ø-å med osm et bogstav, men tal er også med
    #tokenizer = re.compile(r'\W+')
    #string = re.sub(r'\W+',' ', string).lower()
    #tokens = re.sub(r'\d','',string).split()
    #tokens = [token for token in tokens if token > lentoken]
    #tokenizer = re.compile(r'[^a-zA-Z]*') #python 2 version - hverken tal eller æ-ø-å kommer med her
    tokens = [token.lower() for token in tokenizer.split(string) #notice the lowercasing
        if len(token) > lentoken] #splits for each token if len is > 1
    return tokens 

tokens = ''
letters_tokens = []
for text in letters_text_clean:
    tokens = tokenize_text(text,lentoken=2)
    letters_tokens.append(tokens)

print(letters_tokens[0:2])

#### DATAFRAME ALL THE GOOD STUFF
df = pd.DataFrame()

df["text"] = letters_text_clean
df["metadata"] = letters_metadata
df["date"] = letters_dates
df["year"] = letters_years
df["author"] = letters_author
df["recipient"] = letters_recipient
df["tokens"] = letters_tokens

df_sorted = df.sort_values(by=["year","date"], ascending=[True,True])
df.head()


### WORD FREQUENCY

def term_freq(term, tokens):
    """
    Raw term requency
    """
    result = tokens.count(term)
    return result

#### DIVIDE LETTERS INTO PERIODS
period = []
index = 0
for i in df["year"]:
    if i >= "1500" and i < "1600":
        period.insert(index, "1500")
    elif i >= "1600" and i < "1700":
        period.insert(index, "1600")
    elif i >= "1700" and i < "1800":
        period.insert(index, "1700")
    elif i >= "1800":
        period.insert(index, "1800")
    else:
        period.insert(index,"0")
    index = index + 1

#print(period)
#len(df["year"])

df["period"] = period

#### MAKE SLICES FOR EACH PERIOD
six_cen = []
sev_cen = []
eig_cen = []
nin_cen = []
non_cen = [] #list for all the letters without year

index = 0
for token in letters_tokens:
    if period[index] == "1500":
        six_cen.append(token)
    elif period[index] == "1600":
        sev_cen.append(token)
    elif period[index] == "1700":
        eig_cen.append(token)
    elif period[index] == "1800":
        nin_cen.append(token)
    else:
        non_cen.append(token)
    index = index + 1  

len(nin_cen)/len(period)
len(eig_cen)/len(period)
len(sev_cen)/len(period)
len(six_cen)/len(period)

#term frequency of years
lexicon = set(letters_years)
tf_all = dict([(token, letters_years.count(token)) for token in lexicon]) #we make a dictionary of frequency per year

tf_sorted = sorted(tf_all.items()) #and sort it
#print(tf_sorted)


#### SOME VISUALIZATION
os.chdir(wd)

#we join all the letters into one long string
letters_text_sorted = ''
for letter in df_sorted["text"]:
    string = ''.join(letter)

letters_text_sorted = ''.join(df_sorted["text"])

#just a function for dispersion plots
def disp_plot(text,kws, sv=False,):
   """
   dispersion plot for multiple keywords
   """
   kws = [kw.lower() for kw in kws]
   tokens = tokenize_text(text)
   pts = [(x,y) for x in range(len(tokens)) for y in range(len(kws)) if tokens[x] == kws[y]]
   if pts:
       x,y = zip(*pts)
   else:
       x = y = () 
   plt.plot(x,y,"ko")
   plt.yticks(range(len(kws)),kws,color="k")
   plt.ylim(-1,len(kws))
   plt.title("Lexical Dispersion Plot")
   plt.xlabel("Word Offset")
   if sv:
       plt.savefig(filename, dpi = 300)
       plt.show()
       plt.close()
   else:
       plt.show()
       plt.close()

disp_plot(letters_text_sorted,['dansk', 'danske','dansken', 'danskhed', 'danskheden', 'danskere', 'danmark', 'danskerne'],sv=False)
        
print(tf_sorted)

#here we make a list of unique years and a corresponding one with counts for a bar plot
list_years = []
list_freq = []

year = ''
freq = ''
for string in tf_sorted:
    year = string[0]
    freq = string[1]
    list_years.append(year)
    list_freq.append(freq)

qd.plotvars(list_years[1:],list_freq[1:],sv=True)
