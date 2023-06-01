import requests
from bs4 import BeautifulSoup
import httpx
import asyncio
import os
import functools
#This function takes a URL as an argument and collects all the links from the URL
#and put them in a list which then is "cleaned" of any eventual nonetypes.
#it then edits any links that arte incomplete and then returns the list.
async def get_links(adress):
    
    r = httpx.get(adress)
    soup = BeautifulSoup(r.text, 'html.parser')
    links_array = []
    for link in soup.find_all("a"):
        links_array.append(link.get("href"))
    links_array = [i for i in links_array if i is not None]
    for increment in range(len(links_array)):
            holder = links_array[increment]
            if holder.startswith("/"):
                edited_link = adress + links_array[increment]
                links_array[increment] = edited_link
            else:
                continue

    return links_array

#get_text() takes two arguments, a URL and a file name.
#It connects to the website and downloads all the text to a file with the 
#specified file name. 


async def get_text(adress):
    if "https" in adress:
        r = httpx.get(adress)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(adress)
        file_name = os.path.join(os.getcwd() + "/collected_texts", adress.replace("/","") + ".txt")
        with open (file_name, 'w', encoding = "utf-8") as fout:
            fout.write(soup.get_text())
    else:
        print("link is missing https")
    

    	
