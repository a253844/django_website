import requests
from bs4 import BeautifulSoup
import json

class get_sogi_data(object):
    def __init__(self , USER_AGENT_VALUE , query_url , page_url ):
            self.USER_AGENT_VALUE = USER_AGENT_VALUE
            self.query_url = query_url
            self.page_url = page_url

    def Get_brands_url (self):
        headers = {'User-Agent': self.USER_AGENT_VALUE }
        resp = requests.get(self.query_url + self.page_url, headers=headers)
        if not resp:
            print("None")

        resp.encoding = 'UTF-8'
        resp = BeautifulSoup(resp.text, 'html.parser')

        brands_urls = []

        brands = resp.find('div',class_='dropdown-menu dropdown-menu-w100')
        brands = brands.find_all("a" , gacatagory="Header" )

        for i in range(len(brands)):
            brands_tamp = []
            brands_tamp.append(brands[i].text)
            brands_tamp.append(brands[i].get('href'))
            brands_urls.append(brands_tamp)

        brands_urls = brands_urls[:-1]

        return brands_urls

    def Get_brands_products (self , brands_urls):
        headers = {'User-Agent': self.USER_AGENT_VALUE }

        products_urls = []

        for j in range(len(brands_urls[:1])):
            resp = requests.get(self.query_url + brands_urls[j][1], headers=headers)

            resp.encoding = 'UTF-8'
            resp = BeautifulSoup(resp.text, 'html.parser')

            products_hot = resp.find_all("div" , class_='mix-item col-12 col-lg-4 cat2 price4 fcellphone' )
            products = resp.find_all("div" , class_='mix-item col-6 col-sm-3 col-lg-2 cat2 price4 fcellphone' )
            products = products_hot+products

            for i in range(len(products)):
                onsale_product = []
                onsale_product.append(j)
                products_top = products[i].find('span',class_="badge badge-danger pos-a-lt ml-3 mt-3")
                if products_top != None:
                    onsale_product.append(products[i].find("a" , class_="text-row-1" , gacatagory="品牌頁_已上市" ).text)
                    if products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市") == None:
                        onsale_product.append(products[i].find('strong',class_="text-price h6" ).text)
                    else :
                        onsale_product.append(products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市").text)
                    onsale_product.append(products[i].find("a" , class_="text-row-1" , gacatagory="品牌頁_已上市").get('href'))
                elif products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市") == None:
                    break
                else :
                    onsale_product.append(products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市").text)
                    if products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市") == None:
                        onsale_product.append(products[i].find('strong',class_="text-price h6" ).text)
                    else:
                        onsale_product.append(products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市").text)
                    onsale_product.append(products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市").get('href'))
                products_urls.append(onsale_product)

        return products_urls

    def Get_brands_p_detial (self , products_urls):
        headers = {'User-Agent': self.USER_AGENT_VALUE }

        p_detials_list = []

        for product in products_urls[:1]:

            resp = requests.get(self.query_url + product[3], headers=headers)
            resp.encoding = 'UTF-8'
            resp = BeautifulSoup(resp.text, 'html.parser')

            product_detials = resp.find('table', class_="table table-bordered")

            detial_name = product_detials.find_all('th', class_="active")
            detial_content = product_detials.find_all('td')

            detial_name_list= []
            detial_content_list = []
            for i in range(len(detial_name)):
                detial_name_list.append(detial_name[i].text)
                detial_content_list.append(detial_content[i].text)

            p_detial_temp = zip(detial_name_list,detial_content_list)
            p_detials_list.append(dict(p_detial_temp))

        return p_detials_list
