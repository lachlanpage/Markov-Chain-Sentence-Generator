#Markov Sentence Generator 
#By Lachlan Page
import random 

file_string = ""
with open("bleak-house.txt", 'r', encoding='ISO-8859-1') as content_file:
    file_string = content_file.read()

file_string = file_string.split()

#full stop in dictionary to handle end cases
chain = {}
# This line was causing an error later because it made 'key' become a string.
# chain['.'] = ' '
# 'key' needs to be a list which then allows us to use the .append() method later
chain['.'] = [' ']

#More efficient algorith. O(n)
for i in range(0, len(file_string)):
    key = file_string[i]
    if key not in chain:
        # initialize the value of chain[key] to be an empty list
        chain[key] = []
        if(i+1 < len(file_string)):
            chain[key].append(file_string[i+1])
        else:
            chain[key].append('.')
    else:
        #already exists in chain
        if(i+1 < len(file_string)): 
            chain[key].append(file_string[i+1])
        else:
            chain[key].append('.')

#Prediction 
print(len(chain.keys()))
#Can move to dedicated function or something... 
WORD_LENGTH = 10
start_word = random.choice(list(chain.keys()))
final_word_list = []
final_word_list.append(start_word)
for i in range(WORD_LENGTH):
    current_word = final_word_list[i]
    next_word = random.choice(chain[current_word])
    final_word_list.append(next_word)

#Formatting python list to a string for output
result = ''
for word in final_word_list:
    result+= str(word) + " "
print(result)
