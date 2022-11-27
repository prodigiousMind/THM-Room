#!/usr/bin/python3

# THM-ROOM.PY is a simple python script created for educational purpose to
# fetch all the completed rooms of a CTF player

# Author: https://github.com/prodigiousMind

import requests
import json
import time
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'tryhackme.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Upgrade-Insecure-Requests': '1'
}
def help():
    print('''
	\033[92mTHM-ROOM\033[0m: Extract Tryhackme Completed Room Codes/URLs from a player's profile

		[USAGE]:
		python3 thm-room.py [Username | Profile URL]

		\033[96m[eg]: python3 thm-room.py prodigy1337x
		[eg]: python3 thm-room.py https://tryhackme.com/p/prodigy1337x\033[0m
	''')
    
try:
    def write2file(jsonObj):
        '''This function takes an argument (dict type [API response]) and extract different values based on the key, it sends the output to stdout and also saves it in a file'''

        FILE = open("roomInfo.txt", "a")
        for i, j in zip(jsonObj, range(len(jsonObj))):
            dataR = "S.No: " + str(j + 1) + "\n" + "Name: " + i['title'] + "\n" + "Type: " + str(
                i['tags']) + "\nURL: https://tryhackme.com/room/" + str(i['code']) + "\n" + "Room Code: " + str(
                i['title']) + "\n\n"
            print(dataR)
            FILE.write(dataR)

        print("...Rooms detailed file has also been created, see ./roomInfo.txt")
        FILE.close()


    def opener(textResp):
        '''This function taken an argument of str type (response of http request), and convert it into json'''
        rawTx = textResp
        rawTx = json.loads(rawTx)
        write2file(rawTx)


    def dataGrab(url):
        '''This function makes HTTP requests and also checks whether user passed the valid username/URL or not'''

        with requests.session() as sess:

            print("\033[95mFetching Records...\033[0m")
            resp = sess.get(url=url, headers=headers)
            if "Invalid user given" in resp.text:
                print("\033[91mProfile URL does not match\033[0m")
                help()

            else:
                print("\033[95mFetching Completed. Extracting...\033[0m")
                time.sleep(1)
                opener(resp.text)

    option = sys.argv[1]
    u1 = "https://tryhackme.com/api/all-completed-rooms?username="
    u2 = "&limit=2000&page=0"

    if "tryhackme.com" in option:
        username = option.split("/p/")[1]
        username = u1 + str(username) + u2
        dataGrab(username)

    elif option == "help" or option[:2] == "-h":
        help()

    else:
        username = u1 + str(option) + u2
        dataGrab(username)

except:
    print("python3 thm-room.py [Username | User Profile URL]")
    help()
