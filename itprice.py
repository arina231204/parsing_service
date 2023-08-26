
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import quote
import re
async def scrape_data(url, input_str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
        data = {}
        count = 0
        for row in soup.find_all("tr")[1:]:
            cols = row.find_all("td")
            model = cols[1].text.strip().split()[0]
           
            if input_str in model and count < 3:
                new_price = re.sub("[^0-9\.]", "", cols[4].text.strip().split()[0])
                price = re.sub("[^0-9\.]", "", cols[3].text.strip().split()[0])
                item = {
                    "model": cols[1].text.strip(),
                    "description": cols[2].text.strip(),
                    "price": float(price),
                    "source" : cols[1].find("a").get("href"),
                    "photo" : '',
                    "new_price": float(new_price) if new_price else "",
                }
                async with aiohttp.ClientSession() as session2:
                    async with session2.get(cols[1].find("a").get("href")) as response2:
                        soup2 = BeautifulSoup(await response2.text(), "html.parser")
                photo_div = soup2.find("div", class_="details-img")
                if photo_div:
                    photo = photo_div.find("img").get("src")
                else:
                    photo = ""
                item["photo"] = photo
                data[model] = item
                count += 1
        return list(data.values())
    except:
        return []

async def scrape_data_without_newprice(url, input_str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
        data = {}
        count = 0
        for row in soup.find_all("tr")[1:]:
            cols = row.find_all("td")
            model = cols[1].text.strip().split()[0]
            if input_str in model and count < 3:
                price = re.sub("[^0-9\.]", "", cols[3].text.strip())
                item = {
                    "model": cols[1].text.strip(),
                    "description": cols[2].text.strip(),
                    "price": float(price),
                    "source" : cols[1].find("a").get("href"),
                    "new_price":  "",
                }
                async with aiohttp.ClientSession() as session2:
                    async with session2.get(cols[1].find("a").get("href")) as response2:
                        soup2 = BeautifulSoup(await response2.text(), "html.parser")
                photo_div = soup2.find("div", class_="details-img")
                if photo_div:
                    photo = photo_div.find("img").get("src")
                else:
                    photo = ""
                item["photo"] = photo
                data[model] = item
                count += 1
        return list(data.values())
    except:
        return []


async def find_matching_models_cisco(input_str):
    url = f"https://itprice.com/cisco-price-list/{input_str}"
    return await scrape_data(url, input_str)

async def find_matching_models_hp(input_str):
    url = f"https://itprice.com/hp-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)


async def find_matching_models_dell(input_str):
    url = f"https://itprice.com/dell-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)


async def find_matching_models_fortinet(input_str):
    url = f"https://itprice.com/fortinet-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)


async def find_matching_models_juniper(input_str):
    url = f"https://itprice.com/juniper-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)


# async def find_matching_models_huawei(input_str):
    url = f"https://itprice.com/huawei-price-list/{input_str}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
        data = {}
        count = 0
        for row in soup.find_all("tr")[1:]:
            cols = row.find_all("td")
            model = cols[1].text.strip().split()[0]
           
            if input_str in model and count < 3:
                new_price = re.sub("[^0-9\.]", "", cols[4].text.strip().split()[0])
                item = {
                    "model": cols[2].text.strip(),
                    "description": cols[3].text.strip(),
                    "price": cols[4].text.strip().replace('$', '').replace(',', ''),
                    "new_price": cols[5].text.strip() if len(cols) >= 6 else "",
                    "photo": cols[3].find("a")["href"],
          
                }
                  
                async with aiohttp.ClientSession() as session2:
                    async with session2.get(cols[1].find("a").get("href")) as response2:
                        soup2 = BeautifulSoup(await response2.text(), "html.parser")
                photo_div = soup2.find("div", class_="details-img")
                if photo_div:
                    photo = photo_div.find("img").get("src")
                else:
                    photo = ""
                item["photo"] = photo
                data[model] = item
                count += 1
        return list(data.values())
    except:
        return []

 


async def find_matching_models_vmware(input_str):
    url = f"https://itprice.com/vmware-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)
    


async def find_matching_models_dahua(input_str):
    url = f"https://itprice.com/dahua-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)
 

async def find_matching_models_lenovo(input_str):
    url = f"https://itprice.com/lenovo-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)

async def find_matching_models_samsung(input_str):
    url = f"https://itprice.com/samsung-price-list/{input_str}"
    return await scrape_data_without_newprice(url, input_str)



async def find_matching_models_tplink(input_str):
    url = f"https://itprice.com/tplink-price-list/{quote(input_str)}"
    return await scrape_data_without_newprice(url, input_str)

async def find_matching_models_dlink(input_str):
    url = f"https://itprice.com/dlink-price-list/{quote(input_str)}"
    return await scrape_data_without_newprice(url, input_str)

