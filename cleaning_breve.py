# -*- coding: utf-8 -*-

######## ________CLEANING TEXT__________ ##########


# import all modules in beginning of text
import glob, io, os, re, sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO



#################CONVERTING PDF TO TXT AND SAVE

def pdf2txt(path):
    """
    extracts plain text for individual pdf file on path
        - codec: utf-8
        - if embedded password in pdf, password parameter should be updated
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

#save to filepath
def pdf2txt_save(filepath):
    """
    runs and saves output from pdf2txt as ascii (see comment below)
        - modify with io for unicode (the line we're using)
    """
    output = pdf2txt(filepath)
    outname = re.sub("\.pdf",".txt",filepath)
#    with open(outname,"w") as f:
    with io.open(outname, 'w', encoding = 'utf-8') as f:
        f.write(output)

#******* for MULTIPLE files
def pdf2txt_multi(dirpath):
    """
    export all files on directory path to pdf2txt_save
    """
    filelist = glob.glob(dirpath + "/*.pdf")
    for filename in filelist:
        print("conversion of "+ filename.split("/")[-1])
        pdf2txt_save(filename)

def main():
    dirpath = sys.argv[0]
    pdf2txt_multi(dirpath)

if __name__ == '__main__':
       main()

#### for mads' directory
wd = os.getcwd() #absolute path to wd
data_path = '\\letters_without_metadata\\' #relative path to data
os.chdir(wd + data_path)

pdf2txt_multi(os.getcwd())

########### FUNCTIONS FOR READING TEXT FROM FOLDERS
def read_txt(filepath):
    """
    Read txt file from filepath and returns char content in string
    parameters:
        - filepath including filename to file
    """
    with io.open(filepath, 'r', encoding = 'utf-8') as f:
        content = f.read()
    return content
    
def read_dir_txt(dirpath):
    """
    Import multiple txt file from directory on dirpath
    parameters:
        - path to directory as string

    Return list of strings from txt documents in directory
    """
    filenames = glob.glob(dirpath + '*.txt')
    content_list = []
    for filename in filenames:#loop over filenames
        text = read_txt(filename)# read file
        content_list.append(text)# add file to result list
    return content_list, filenames# return two lists, file content

######## TOKENIZING AND CLEANING

def tokenize(text, lentoken = 0):
    """
    string tokenization and lower-casing for text string
    parameters:
        - text: string to be tokenized
        - lentoken: ignore tokens shorter than or equal to lentoken (default: 0)
    """
    tokenizer = re.compile(r'[^a-zA-Z]+')
    tokens = [token.lower() for token in tokenizer.split(text)
        if len(token) > lentoken]
    return tokens


       
    
    
    
    
    
    
    
    
    
    







