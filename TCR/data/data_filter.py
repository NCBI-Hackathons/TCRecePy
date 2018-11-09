# Constants
range_of_strings = 30


# Loads the data from a file and outputs it into corresponding directory

print("Input the desired file for processing:")
file_name = input()

# Input file and data
f = open(file_name+".txt","r")
strings_list = f.read().split("\n")
f.close()

# Locations for the strings that will be used
outputs = dict()
for i in range(range_of_strings): outputs[i] = [] # Assigning a new list to each string size

# Sorting the strings
for s in strings_list:
    if len(s) < range_of_strings:
        outputs[len(s)].append(s)

# Outputting the string groups to files
for i in range(range_of_strings):
    if (len(outputs[i]) > 0):
        outfile = open("processed_data/"+file_name+"/"+file_name+"_"+str(i)+".txt","w+")
        outfile.write("\n".join(outputs[i]))
        outfile.close()
