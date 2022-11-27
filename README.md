# THM-Room
THM-ROOM.PY is a python script created for educational purpose to fetch all the completed Tryhackme rooms details of a CTF player

> Usage `python3 thm-room.py help`
## It can also be used with commands such as `grep`|`sed` to extract only Room URLs/Codes
### Example:
> python3 thm-room.py [username/url] | sort | uniq | grep -i "url"

> python3 thm-room.py [username/url] | sort | uniq | grep -i "code:"
### The above first command will only show Room's URL and the second one will show Room's code
