import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import aiohttp
from tweakers import get_exchange_eur_to_usd_rate

async def parse_data_microforce(input_str):
   url = f"https://www.microforce.be/search/{quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')

      products = []
      product_containers = soup.find_all('div', {'class': 'product-item-info'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         container = product_containers[i]
         name = container.find('strong', {'class': 'product name product-item-name'}).text.strip()
         price = container.find('span', {'class': 'price-wrapper'}).text.strip()
         price = price.replace(".", "")
         price_str = re.sub(r'[^\d.,]+', '', re.sub(r'[€-]+', '', price))
         price_str = price_str.replace(",", ".") 
         if price_str[-1] == '.':
            price_str = price_str + '00'
         price_gbp = float(price_str)
         price_usd = price_gbp * await get_exchange_eur_to_usd_rate()
         img_url = container.find('img', {'class': 'product-image-photo'})['src']
         source = container.find('a', {'class': 'product-item-link'})['href']
         products.append({
               'name': name, 
               'description': name, 
               'price': round(price_usd, 2),
               'source': source,
               'photo': img_url,
               'new_price': ""
          })
         i += 1
      return products
   except:
      return []