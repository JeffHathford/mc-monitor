import matplotlib.pyplot as plt
import json, os

def enter_query():
  enter = {''}

  while(True):
    choice = input().lower()
    if choice in enter:
      return True
    else:
      return False


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


    except (FileNotFoundError, json.decoder.JSONDecodeError):   #if there is no file, end
        print(f"File {filename} does not exist or is corrupted.")
        exit("\nProgram has ended.")

data_dict = data["hours"]
data_dict = {float(key):value for key, value in data_dict.items()}
data_dict2 = sorted(data_dict.items())

dummy_data = data_dict2[0]
dummy_data = (24.0, dummy_data[1])

data_dict2.append(dummy_data)


x_list = []
y_list = []

for tup in data_dict2:
    x_list.append(float(tup[0]))
    y_list.append(tup[1])

y_list = [round(sum(a)/len(a), 2) for a in y_list]

print(x_list)
print(y_list)

x = x_list
y = y_list
  

plt.plot(x, y) 

plt.grid(True)

plt.ylim(0, data["max players"]) 
plt.xlim(0, 24)

plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])


plt.xlabel('Time of day') 
plt.ylabel('Players') 
plt.title(f'{data["name"]}\n{data["address"]}') 
  

plt.show() 