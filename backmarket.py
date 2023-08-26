import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

async def parse_data_backmarket(input_str):
   url = f"https://www.backmarket.com/en-us/search?q={quote(input_str)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               soup = BeautifulSoup(await response.text(), 'html.parser')
      products = []
      product_containers = soup.find_all('div', {'class': 'grid grid-cols-1 gap-4 md:gap-7 lg:grid-cols-[repeat(3,26.2rem)] md:grid-cols-[repeat(2,26.2rem)]'})
      for container in product_containers[:3]:
         name = container.find('img')['alt']
         price = container.find('span', {'class': 'body-2-bold text-black'}).text.strip().replace('$', '')
         img_url = container.find('img')['src']
         source = container.find('a', {'class': 'focus:outline-none group md:box-border relative'})['href']
         description = name
         products.append({'name': name, 'description': description, 'price': price , 'source': f'https://www.backmarket.com/{source}', 'photo': f'https://www.backmarket.com/{img_url}', 'new_price': ''})
      return products
   except:
      return []

