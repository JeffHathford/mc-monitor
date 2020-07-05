import json, os, sys

def merge_dols(dol1, dol2):
    keys = set(dol1).union(dol2)
    no = []
    return dict((k, dol1.get(k, no) + dol2.get(k, no)) for k in keys)


data1 = None
data2 = None
data_final = None

if len(sys.argv) < 4:
    exit("Please provide at least three files.\nThe program has ended.")

file1 = sys.argv[1]
file2 = sys.argv[2]
file_final = None


if len(sys.argv) == 4:
    file_final = sys.argv[3]

if not file1.endswith(".txt"):
    file1 = file1 + ".txt"

if not file2.endswith(".txt"):
    file2 = file2 + ".txt"

if not file_final.endswith(".txt"):
    file_final = file_final + ".txt"


while(True):
    try:
        with open(file1, 'r') as textfile1:
            data1 = json.load(textfile1)
        
        with open(file2, 'r') as textfile2:
            data2 = json.load(textfile2)

        if data1 is not None and data2 is not None:
            break

    except (FileNotFoundError, json.decoder.JSONDecodeError):   #if there is no file, end
        print(f"An error has occured.")
        exit("\nThe program has ended.")

for item in ["url", "name", "address", "max players"]:
    if data1[item] != data2[item]:
        print(f"Data mismatch.")
        exit("\nThe program has ended.")
    


#combined = {key:data1["hours"][key] + data2["hours"][key] for key in data1["hours"]}
data_final = data1
data_final["hours"] = merge_dols(data1["hours"], data2["hours"])


with open(file_final, 'w+') as outfile:
    json.dump(data_final, outfile, indent=4)
    print("\nMerging files was successful!")