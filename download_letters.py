# -*- coding: utf-8 -*-
from urllib.request import urlopen as uReq
import requests, os
from bs4 import BeautifulSoup as soup

###### GET LIST OF BOOKS #######
my_url_books = 'http://danmarksbreve.kb.dk/brevudgivelser'

#opens connection, grabs the page
client_books = uReq(my_url_books)
page_html_books = client_books.read()
client_books.close()

#parses into html
page_soup_books = soup(page_html_books, "html.parser")

#we get the html of of all books on the website.
containers_books = page_soup_books.findAll("div", {"itemtype":"http://schema.org/Thing"}) #grabs all html objects to a list

#we get the ID for every book and append it to a list 
books_list=[]
for container in containers_books:
    book = container.a["data-context-href"]
    if len(books_list) < 91:
        books_list.append(book[:-6])

###### GET LIST OF LETTERS ########

#we get a list of all the urls for the books
my_url_letters = 'http://danmarksbreve.kb.dk'
urls_books=[]
for book in books_list:
    url = my_url_letters + book
    urls_books.append(url)

letters_list=[] #we make a list for all the letters
for url in urls_books: #we repeat the same process for all urls
    client = uReq(url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("a") #here we get a list of all letters for each book
    for container in containers:
        link = container["href"]
        if len(letters_list) < 20000:
            if len(my_url_letters + '/catalog' + link) > 90:
                if not ("-idm" in link):
                    letters_list.append(my_url_letters + '/catalog' + link[1:] + '.pdf') #we append the ID of all letters to one big list
            
print(len(letters_list))
print(len(set(letters_list)))
print(letters_list[0])

wd = os.getcwd()
data_path = '\\letters_without_metadata' #relative path to data
os.chdir(wd + data_path)


for link in letters_list: #for each link download the pdf
    response = requests.get(link)
    with open(link[51:], 'wb') as f: #filename is the unique ID of every letter
        f.write(response.content)