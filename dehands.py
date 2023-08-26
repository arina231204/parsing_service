import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from tweakers import get_exchange_eur_to_usd_rate

async def parse_data_2dehands(input_str):
   url = f"https://www.2dehands.be/q/{quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')
      products = []
      product_containers = soup.find_all('li', {'class': 'hz-Listing hz-Listing--list-item'})
      i = 0
      while len(products) < 3 and i < len(product_containers):
         for container in product_containers[:3]:
            if container is None or len(products) >= 3:
               break
            name = container.find('h3', {'class': 'hz-Listing-title'}).text.strip()
            
            price = container.find('span', {'class': 'hz-Listing-price hz-text-price-label'}).text.strip()
            price = price.replace(",", ".")
            price_str = re.sub(r'[^\d.,]+', '', re.sub(r'[€-]+', '', price))
            price_gbp = float(price_str)
            price_usd  = price_gbp * await get_exchange_eur_to_usd_rate()
            img_url = container.find('img')['src']
            source = container.find('a')['href']
            products.append({'name': name, 'description': name, 'price': round(price_usd, 2) , 'source': f'https://www.2dehands.be{source}', 'photo': img_url, 'new_price': ''})
         i += 1
      return products
   except:
      return[]
   