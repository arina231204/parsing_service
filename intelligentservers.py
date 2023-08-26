import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
async def get_exchange_rate():
   url = 'https://wise.com/ru/currency-converter/gbp-to-usd-rate'
   async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
         html = await response.text()
   soup = BeautifulSoup(html, 'html.parser')
   exchange_rate_span = soup.find('span', {'class': 'text-success'})
   exchange_rate_str = exchange_rate_span.text.strip()
   exchange_rate = float(re.sub(r'[^\d.]', '', exchange_rate_str))
   return exchange_rate

async def parse_data_intelligentservers(query):
   url = f"https://intelligentservers.co.uk/filterSearch?q={quote(query)}"
   try:
      async with aiohttp.ClientSession() as session:
         async with session.get(url) as response:
               html = await response.text()
      soup = BeautifulSoup(html, "html.parser")
      items = soup.find_all("div", class_="item-box")
      result = []
      i = 0
      while len(result) < 3 and i < len(items):
         item = items[i]
         title = item.find("h2", class_="product-title").text.strip()
         img = f"https://intelligentservers.co.uk/{item.find('img')['src']}"
         price_span = item.select_one('.prices .actual-price') 
         price_span = '' if price_span and price_span.text.strip() == 'Call for pricing: +44(0)1423 223430' else price_span
         source = f'https://intelligentservers.co.uk{item.find("h2", class_="product-title").find("a")["href"]}'
         if price_span  :
               price_str = re.sub(r'[^\d.]+', '', price_span.text)
               price_gbp = float(price_str)  
               exchange_rate = await get_exchange_rate()
               price_usd = price_gbp * exchange_rate
               result.append({
                  "name": title,
                  "description": title,
                  "price": round(price_usd, 2),
                  'source': source,
                  "photo": img,
                  'new_price': "",
               })
         i += 1
      
      return result
      
   except Exception as e:
      return []
