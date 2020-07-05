import os, sys, requests
import time, json
from bs4 import BeautifulSoup

URL_CONST = 7

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 

    else: 
        _ = os.system('clear') 

def yes_no_query():
  yes = {'y', 'yes', 'ye', ''}
  no = {'no','n'}

  while(True):
    choice = input().lower()
    if choice in yes:
      return True
    elif choice in no:
      return False
    else:
      sys.stdout.write("Please respond with 'yes' or 'no'\t")

def read_monitor_query():
  read = {'read', 'r', 'rea'}
  monitor = {'monitor','monit','m'}

  while(True):
    choice = input().lower()
    if choice in read:
      return True
    elif choice in monitor:
      return False
    else:
      sys.stdout.write("Please respond with 'read' or 'monitor'\t")

def enter_query():
  enter = {''}

  while(True):
    choice = input().lower()
    if choice in enter:
      return True
    else:
      return False


#main

#clear the console window
clear()

#load the saved url, ask if it's okay, do changes and start the monitor
print("Default file: stored_data.txt\nPress Enter to continue or input anything to select another file:\n")
if enter_query() == False:
    print("\nPlease specify the name of file you want to use:\n")
    filename = input()
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
else:
    filename = "stored_data.txt"

#load the json file
data = None

while(True):
  try:
      with open(filename, 'r') as textfile:
          data = json.load(textfile)
          if "url" not in data or not data["url"]:
              raise FileNotFoundError
          else:
              break


  except (FileNotFoundError, json.decoder.JSONDecodeError):   #if there is no file, input new url
      print(f"File {filename} does not exist or is corrupted, do you want to create a new one? Y/n")
      if yes_no_query() == False:
          exit("Program has ended.")

      print("Please input the url of the Minecraft server you want to monitor:\n")
      url = input()
      data = {
        "url": str(url),
        "name": "",
        "address": "",
        "max players": 0,
        "hours": {}
        }
      with open(filename, 'w') as outfile:
          json.dump(data, outfile, indent=4)

#request the webpage data
clear()
print(f"Currently used url: {data['url']}\n")

print("Do you want to launch the monitor or get a single data read?\tmonitor/read")
if read_monitor_query() == True:    #single read
    res = requests.get(data['url'])
    soup = BeautifulSoup(res.text, 'html.parser')

    server_name = (soup.find("h1").string)
    server_ip = (soup.find(string = "Address").parent.parent.parent.contents[3].string)

    player_string = (soup.find(string = "Players").parent.parent.parent.contents[3].string)
    players = int(player_string.split("/")[0])
    max_players = int(player_string.split("/")[1])

    clear()
    print(f"Server name: {server_name}\nAddress: {server_ip}\n")
    print(f"Players: {players}\nMax players: {max_players}\n")


else:                               #monitor
    while(True):
        t = time.localtime()
        current_time = time.strftime("%H:%M", t)
        print(f"Running: {current_time}", end="\r")

        if t.tm_min % 15 == 0:   #get data
            


            res = requests.get(data['url'])
            soup = BeautifulSoup(res.text, 'html.parser')

            server_name = (soup.find("h1").string)
            server_address = (soup.find(string = "Address").parent.parent.parent.contents[3].string)

            player_string = (soup.find(string = "Players").parent.parent.parent.contents[3].string)

            players = int(player_string.split("/")[0])
            max_players = int(player_string.split("/")[1])

            data["name"] = server_name
            data["address"] = server_address
            data["max players"] = max_players

            time_formatted = str( float(t.tm_hour) + round(float(t.tm_min/60), 2) )

            if time_formatted not in data["hours"]:
                data["hours"][time_formatted] = []
            data["hours"][time_formatted].append(players)

            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("\nCheck successful!")

        time.sleep(60)
