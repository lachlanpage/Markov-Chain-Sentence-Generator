#Markov Sentence Generator 
#By Lachlan Page
import random 

file_string = ""
with open("book.txt", 'r') as content_file:
    file_string = content_file.read()
file_string = file_string.split()
#Only a subset of text need to optimize to quicken results
file_string = file_string[:10000]

#full stop in dictionary to handle end cases
chain = {}
chain['.'] = ' '

#two passes first for finding keys, second pass for finding tokens
for key in file_string: 
    if key not in chain:
        chain[key] = []

#For token in dict, iterate through file_string for occurance of token, get next word and append to list. If not in bounds append '.'
for token in chain:
    token_list = []
    for i in range(0, len(file_string)):
        if(token == file_string[i]):
            if(i+1) >= len(file_string):
                #If out of bounds include full stop. Should fix this to use something else. 
                token_list.append(".")
            else:
                token_list.append(file_string[i+1])
    chain[token] = token_list

#Prediction 
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
