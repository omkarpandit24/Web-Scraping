from bs4 import BeautifulSoup
import re

def read_file():
    file = open('product_names.txt')
    data = file.read()
    file.close()
    return data


soup = BeautifulSoup(read_file(),'lxml')
#Part 1 Find out all product names
all_as = soup.find_all('a', attrs = {'class': 'products-a-z__results__item'})


product_names = [a.string for a in all_as]

for product_name in product_names:
    print(product_name)
    
    
#Part 2 Find out all product names with their indivisual urls

product = {} #product name - key ; url - value
all_as = soup.find_all('a', attrs = {'class': 'products-a-z__results__item'})

product_names = [a.string for a in soup.find_all('a', attrs = {'class': 'products-a-z__results__item'})]

product_links = [a['href'] for a in soup.find_all('a', attrs = {'class': 'products-a-z__results__item'})]

for link in product_links:
    print(link)

#another way
product = {a.string:a['href'] for a in soup.find_all('a', attrs = {'class': 'products-a-z__results__item'})}

for key,value in product.items():
    print(key,'  --->', value)









    