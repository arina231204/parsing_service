from fastapi import FastAPI
from deepdiscountservers import parse_data_deepdiscountservers
from intelligentservers import parse_data_intelligentservers
from microforce import parse_data_microforce
from refurbished import parse_data_refurbishedbe
from tweakers import parse_data_tweakers
from ultratec import parse_data
from backmarket import parse_data_backmarket
from itprice import *
from fastapi import FastAPI
from typing import List
from ebay import parse_data_ebay
from dehands import parse_data_2dehands
app = FastAPI()
import asyncio
import asyncio

@app.get("/{input_str}")
async def find_matching_models_all(input_str: str):
   funcs = [
      find_matching_models_cisco, 
      find_matching_models_hp, 
      find_matching_models_dell, 
      find_matching_models_fortinet, 
      find_matching_models_juniper, 
      find_matching_models_vmware,
      find_matching_models_dahua,
      find_matching_models_lenovo,
      find_matching_models_samsung,
      find_matching_models_tplink,
      find_matching_models_dlink,
      parse_data_deepdiscountservers,
      parse_data_intelligentservers,
      parse_data_microforce,
      parse_data_refurbishedbe,
      parse_data_tweakers,
      parse_data,
      parse_data_backmarket,
      parse_data_ebay,
      parse_data_2dehands

      
   ]
   tasks = [asyncio.create_task(func(input_str)) for func in funcs]
   results = await asyncio.gather(*tasks, return_exceptions=True)
   flattened_results = [d for sublist in results for d in sublist if isinstance(sublist, list)]
   return flattened_results
 




