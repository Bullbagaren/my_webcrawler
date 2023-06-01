from handle_requests import get_links
from handle_requests import get_text
import sys
import os
import asyncio
import functools
from multiprocessing import Pool 
#The main function checks for an argument that was passed along with the calling of the script.
#if this argument is a file it then read each line from the file and passes it to the 
# collect_text() function. If not it treats the argument as a URL and passes only that to the collect_text() function
async def main():
    adress_name = sys.argv[1]
    if os.path.exists(str(os.getcwd()) + "/" + adress_name):
        with open(adress_name) as fin:
            for line in fin:
                print(line)
                line = line.strip("\n")
                await collect_text(line)

    else:
        await collect_text(adress_name)



#This is the is the workhorse of the program, it collects the list of links from the get_links() functions 
#creates a directory to save the files in, it then itterates throught the link list and saves the text from 
#each in link in a seperate file in the created directory. If the link doesn't have https in it,
#it will not run it since it's likly a broken link or a link that didn't get edited properly in the 
#get_links() function. This isn't the best solution since it allows links with https further into the URL 
#to slip through the detection and can cause an error, however it's unlikely.
async def collect_text(adress_name):

    links_array = await get_links(adress_name)
    current_dir = os.getcwd()
    new_dir = current_dir + "/collected_texts/"
    path = os.makedirs(new_dir, exist_ok=True)
    file_name = adress_name.split(".", 1)
    file_name = str(adress_name[1])
    links_array = set(links_array)
    await get_text(adress_name)
    with Pool() as pool:
        for link in links_array:
            results = pool.imap(await get_text(link), links_array)
    #tasks = [asyncio.create_task(get_text(link)) for link in links_array ]
    #done, pending = await asyncio.wait(tasks)


    #for link in links_array:
     #   print(link)
       # text_name = os.path.join(new_dir, link.replace("/","") +".txt")
       # if "https" in link:
        #   await get_text(link, text_name)


if __name__ == '__main__':
        
    asyncio.run(main())
