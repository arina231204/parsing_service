import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

async def parse_data_ebay(input_str):
   url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')
      products = []
      product_containers = soup.find_all('div', {'class': 's-item__info clearfix'})
      product_containers2 = soup.find_all('div', {'class': 's-item__image-wrapper image-treatment'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         for i, container in enumerate(product_containers):
            if len(products) >= 3:
                  break
            name = container.find('div', {'class': 's-item__title'}).text.strip()
            description = container.find('div', {'class': 's-item__subtitle'}).text.strip()
            price = container.find('span', {'class': 's-item__price'}).text.strip().replace('$', '')
            source = container.find('a')['href']
            img_url = product_containers2[i].find('img')['src']
            if "Shop on eBay" not in name:
                  products.append({'name': name, 'description': description, 'price': float(price) , 'source': source, 'photo': img_url, 'new_price': ''})
         i += 1
      return products
   except:
      return []






