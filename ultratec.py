import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
from intelligentservers import get_exchange_rate
import aiohttp

async def parse_data(input_str):
   url = f"https://shop.ultratec.co.uk/search/?searchfor={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               html = await response.text()

      soup = BeautifulSoup(html, 'html.parser')

      products = []
      product_containers = soup.find_all('article', {'class': 'card card-product'})
      i = 0

      while len(products) < 3 and i < len(product_containers):
         container = product_containers[i]
         name = container.find('h4', {'class': 'title'}).text.strip()
         description = container.find('p').text.strip() if container.find('p').text.strip() else name
         price = container.find('span', {'class': 'price'})
         source = container.find('a', {'class': 'btn btn-secondary'})['href']

         if price:
               price = price.text.strip()
               price_str = re.sub(r'[^\d.]+', '', re.sub(r'£', '', price))
               price_gbp = float(price_str) if price_str else 0
               price_usd  = await get_exchange_rate()
               if price_usd != 0.0:
                  img_url = f"https://shop.ultratec.co.uk/{container.find('img')['src']}" if container.find('img')['src'] != "/images/noimage.png" else ""
                  products.append({'name': name, 'description': description, 'price': round(price_usd, 2), 'source': f"https://shop.ultratec.co.uk{source}", 'photo': img_url, 'new_price': ""})
         i += 1

      return products[:3]

   except Exception as e:
      return []
# print(parse_data('cisco'))
