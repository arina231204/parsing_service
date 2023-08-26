import asyncio
import aiohttp
import re
from urllib.parse import quote
from bs4 import BeautifulSoup


async def parse_data_deepdiscountservers(input_str):
   url = f"https://deepdiscountservers.com/catalogsearch/result/?q={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')
      products = []
      product_containers = soup.find_all('div', {'class': 'product-item-info'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         for container in product_containers[:3]:
            
               name = container.find('a', {'class': 'product-item-link'}).text.strip()
               price = container.find('span', {'class': 'price'}).text.strip()
               price_str = re.sub(r'[^\d\.]', '', price)
               price_gbp = float(price_str)
               img_url = container.find('img')['src']
               source = container.find('a', {'class': 'product-item-link'})['href']
               async with aiohttp.ClientSession() as session2:
                  async with session2.get(source) as response2:
                     soup2 = BeautifulSoup(await response2.text(), 'html.parser')
               description = soup2.find('p', {'class': 'just'}).text.strip()
               products.append({'name': name, 'description': description, 'price': price_gbp, 'source': source, 'photo': img_url, 'new_price': ''})
         i += 1
      return products
   except:
      return []


# print(parse_data_deepdiscountservers('S'))