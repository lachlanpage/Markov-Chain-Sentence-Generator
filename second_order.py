#Markov Model Second Order Sentence Generator 
#By Lachlan Page
import random 

file_string = ""
with open("book.txt", 'r') as content_file:
    file_string = content_file.read()
file_string = file_string.lower()
file_string = file_string.split()
#Only a subset of text need to optimize to quicken results
file_string = file_string[:10000]

#full stop in dictionary to handle end cases
chain = {}
chain['.'] = ' '

#two passes first for finding keys, second pass for finding tokens
for i in range(0, len(file_string)):
    key = file_string[i]
    next_key = "."
    if(i+1 < len(file_string)):
        next_key = file_string[i+1]
    
    pair = (key, next_key)
    if pair not in chain:
        chain[pair] = []

#For token in dict, iterate through file_string for occurance of token, get next word and append to list. If not in bounds append '.'
#token is a tuple
for token in chain:
    token_list = []
    for i in range(0, len(file_string)):
        if(token[0] == file_string[i]):
            #check second part of character
            if((i+1) < len(file_string)):
                if(token[1] == file_string[i+1]):
                    if(i+2 < len(file_string)):
                        token_list.append(file_string[i+2])
                    else:
                        token_list.append(".")
            else:
                token_list.append(".")
    chain[token] = token_list

#prediction
WORD_LENGTH = 25
start_word = random.choice(tuple(chain.keys()))
final_word_list = []
current_tuple = start_word

for i in range(WORD_LENGTH):
    current_word = current_tuple
    next_word = random.choice(chain[current_word])
    current_tuple = (current_word[1], next_word)
    final_word_list.append(next_word)

result = ''
for word in final_word_list:
    result+= str(word) + " " 
print(result)
