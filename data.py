import pandas as pd
from bs4 import BeautifulSoup
import requests


def user_search(user_input_search_term):
    """Creates a BeautifulSoup html object 
       and parses the html text to find the total number of pages 
       
       :param user_input_search_term: search term provided by the user
       :returns:
            - pages - total number of pages or 0 if there are no pages found  
            - doc - BeautifulSoup object or 'Nothing Found' if nothing could be found by 
                    the user_input_search_term provided
    """
    search_term = user_input_search_term.rstrip().lstrip().replace(' ', '+')   
    url = f'https://www.newegg.com/p/pl?d={search_term}&N' #Products that are only in stock url
    doc_html = requests.get(url).text
    doc = BeautifulSoup(doc_html, "html.parser") 
    if doc.find('span', attrs ={'class':'list-tool-pagination-text'}):
        page_number_text = doc.find('span', class_ = 'list-tool-pagination-text').find('strong', recursive=False)#Find the direct child of 
        pages = int(str(page_number_text).split("/")[1].split('>')[1][:-1])
        return(pages, doc)
    else:
        return(0,'Nothing Found') 

def get_data(pages, doc):
    """Extracts html text and creates a dataframe. 
       The dataframe is created by extracting specific html text and storing it in specific lists. 
       Those lists are then stored in a dictionary which is then used to create a dataframe 
       
       :param pages:Total number of pages
       :param doc: BeautifulSoup html object
       :returns:
            - df - dataframe
    """
    search_dictionary={} # all lists will be stored in this dictionary to creare a dataframe
    link_list=[] #hyperlink of item
    details_list=[] #details/description of item
    total_cost_list=[] #price of item
    shipping_price_list=[] #shipping price 
    rating_list=[] # rating of item
    number_of_reviews_list=[] #number of reviews
    pages_list=[] #page where item is found

    div = doc.find_all('div', class_= 'item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
    for pages in range(1, pages+1):
        for div_item in div:
            for x in div_item:
                if x.find('a', attrs ={'href':True}):
                    link = x.find('a')['href']
                    link_list.append(link)
                else:
                    link_list.append('None')
                if x.find('a', attrs ={'title':True}):
                    details = x.find('a', title= 'View Details').string
                    details_list.append(details)
                else:
                    details_list.append('None')
                if  x.find('span', class_='price-current-label'):
                    price_dollars = x.find('li', class_='price-current').find('strong').string
                    price_cents = x.find('li', class_= 'price-current').find('sup').string
                    total_cost = '$'+price_dollars+price_cents
                    total_cost_list.append(total_cost)
                else:
                    total_cost_list.append('None')
                if x.find('li', class_= 'price-ship'):
                    shipping_price= x.find('li', class_= 'price-ship').string
                    shipping_price_list.append(shipping_price)
                else:   
                    shipping_price_list.append('None')  
                if x.find('i', attrs ={'aria-label':True}) : #attrs is a like a dictionary {key:value}
                    rating = x.find('i', class_= 'rating')['aria-label']
                    rating_list.append(rating)
                    reviews = x.find('span', class_= 'item-rating-num').string
                    number_of_reviews = reviews.split(')')[0].split('(')[1]
                    number_of_reviews_list.append(number_of_reviews)
                else:
                    rating_list.append('None')
                    number_of_reviews_list.append('None')
                pages_list.append(pages)
    search_dictionary= {"hyperlink":link_list, 'details':details_list, 'price':total_cost_list, 
                        'shipping price':shipping_price_list, 'rating':rating_list, 'number of reviews':number_of_reviews_list, 'page found': pages_list}             
    df = pd.DataFrame.from_dict(search_dictionary)
    return(df)