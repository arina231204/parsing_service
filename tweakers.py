import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import aiohttp
async def get_exchange_eur_to_usd_rate():
   url = 'https://wise.com/ru/currency-converter/eur-to-usd-rate'
   async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
         soup = BeautifulSoup(await response.text(), 'html.parser')
   exchange_rate_span = soup.find('span', {'class': 'text-success'})
   exchange_rate_str = exchange_rate_span.text.strip()
   exchange_rate = float(re.sub(r'[^\d.]', '', exchange_rate_str))
   return exchange_rate

async def parse_data_tweakers(input_str):
   url = f"https://tweakers.net/pricewatch/zoeken/?keyword={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')

      products = []
      product_containers = soup.find_all('tr', {'class': 'largethumb'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         container = product_containers[i]
         name = container.find('a', {'class': 'editionName'}).text.strip()
         description = container.find('p', {'class': 'specline'})
         if description:
               description = description.text.strip()
         price = container.find('p', {'class': 'price'})
         if price:
               price = price.text.strip()
               price = price.replace(".", "")
               price_str = re.sub(r'[^\d.,]+', '', re.sub(r'[€-]+', '', price))
               price_str = price_str.replace(",", ".") 
               if price_str[-1] == '.':
                  price_str = price_str + '00'
               price_gbp = float(price_str)
               price_usd  = price_gbp * await get_exchange_eur_to_usd_rate()
               img_url = container.find('img')['src']
               source = container.find('a', {'class': 'editionName'})['href']
               products.append({'name': name, 'description': description, 'price': round(price_usd, 2), 'source': source, 'photo': img_url, 'new_price': ""})
         i += 1
      return products[:3]
   except:
      return []







# print(parse_data_tweakers('hp 16GB'))
