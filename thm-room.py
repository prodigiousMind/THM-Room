#!/usr/bin/python3

# THM-ROOM.PY is a python script created for educational purpose to
# fetch all the completed rooms of a CTF player, and to automate room joining

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

        \033[96m[eg]: python3 thm-room.py username
        [eg]: python3 thm-room.py https://tryhackme.com/p/username\033[0m
    ''')
 
try:

    def jr(codeList):

        codeList.sort()
        sjoin = 0
        sfail = 0
        cookMe = input("Enter cookie value (extract from request headers): ")
        if (str(cookMe[:7]).lower() == "cookie:"):
            cookMe = cookMe.split("Cookie: ")[1]
        headers['Cookie'] = cookMe.strip()
        print("\033[93mExtracting Unjoined Rooms\033[0m")
        resp = requests.get(url="https://tryhackme.com/api/my-rooms?limit=5000", headers=headers)
        jsonRoom = json.loads(resp.text)['rooms']
        
        myRooms = []

        for room in jsonRoom:
            myRooms.append(str(room['code']))
        myRooms.sort()
        
        uniqueCode = set(codeList) - set(myRooms)
        uniqueCode = list(uniqueCode)
        uniqueCode.sort()


        for c in uniqueCode:
            resp = requests.get(url="https://tryhackme.com/jr/"+str(c), headers=headers)

            # delay is required, in case frequent requests gets blocked
            time.sleep(0.3)
            if "tryhackme.com/room/" in resp.url or "/network/" in resp.url:
                sjoin += 1
                print("\033[96m[+]\033[0m tryhackme.com/room/{} - Joined".format(c))
            else:
                sfail += 1
                print("\033[91m[-]\033[0m tryhackme.com/room/{} - Room joining failed".format(c))
        print("{}/{} room joined".format(sjoin, len(uniqueCode)))
        

    def write2file(jsonObj):
        '''This function takes an argument (dict type [API response]) and extract different values based on the key, it sends the output to stdout and also saves it in a file'''
        listOfCode = []
        FILE = open("roomInfo.txt", "a")
        for i, j in zip(jsonObj, range(len(jsonObj))):
            dataR = "S.No: " + str(j + 1) + "\n" + "Name: " + i['title'] + "\n" + "Type: " + str(
                i['tags']) + "\nURL: https://tryhackme.com/room/" + str(i['code']) + "\n" + "Room Code: " + str(
                i['code']) + "\n\n"
            listOfCode.append(str(i['code']))
            FILE.write(dataR)

        print("...Rooms detailed file has also been created, see ./roomInfo.txt")
        FILE.close()
        print("\n\033[92mWould you like to join the fetched groups as well?\033[0m")
        opt = input("1-> Yes or 2-> No: ")
        jr(listOfCode) if (opt == "1" or opt.lower() == "yes" or opt.lower() == "Y") else print('terminating...')


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
    u2 = "&limit=5000&page=0"

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

