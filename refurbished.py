import re
import requests
from bs4 import BeautifulSoup 
import aiohttp
from urllib.parse import quote
from tweakers import get_exchange_eur_to_usd_rate


async def parse_data_refurbishedbe(input_str):
   url = f"https://www.refurbished.be/zoeken?product={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')
      products = []
      product_containers = soup.find_all('div', {'class': 'productContent'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         container = product_containers[i]
         name = container.find('div', {'class': 'productTitle fn'}).text.strip()
         description = container.find('div', {'class': 'productTitle fn'}).text.strip()
         price = container.find('div', {'class': 'productPrice price'}).text.strip()
         price = price.split()[1] 
         price = price.replace(".", "").replace(",", ".")
         price_str = re.sub(r'[^\d\.]', '', price)
         price_gbp = float(price_str)
         price_usd = price_gbp * await get_exchange_eur_to_usd_rate()
         source = container.find('div', {'class': 'productTitle fn'}).find('a')['href'].strip()
         containers = soup.find_all('div', {'class': 'productImage photo'})
         for container in containers:
               pictures = container.find_all('picture')
               for picture in pictures:
                  img_url = picture.find('img')['src']
         products.append({
               'name': name, 
               'description': description, 
               'price': round(price_usd, 2), 
               'source': source, 
               'old_price': '', 
               'photo': img_url
         })
         i += 1
      return products
   except Exception as e:
      return []




# print(parse_data_refurbishedbe('HP 512744-001'))
