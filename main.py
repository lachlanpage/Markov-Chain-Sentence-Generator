#Markov Sentence Generator 
import random 
tester = ""
with open("book.txt", 'r') as content_file:
    tester = content_file.read()
tester = tester.split()
tester = tester[:10000]
#tester = "do you like green eggs and ham? I do like green legs and sam"
#tester = tester.split()
#two passes one for finding keys, second pass for finding tokens

chain = {}
chain['.'] = ' '
for key in tester: 
    if key not in chain:
        chain[key] = []


#for value in dictionary, iterate through text for occurance of value, get next word and append to list
i = 0
for token in chain:
    token_list = []
    for ind in range(0, len(tester)):
        if(token == tester[ind]):
            if(ind+1) >= len(tester):
                #bout to go out of bounds need to include start and end bits
                #To fix
                token_list.append(".")
            else:
                token_list.append(tester[ind+1])
    chain[token] = token_list
    i = i + 1
    #

WORD_LENGTH = 1000
start_word = random.choice(list(chain.keys()))
final_word_list = []
final_word_list.append(start_word)

for i in range(WORD_LENGTH):
    current_word = final_word_list[i]
    next_word = random.choice(chain[final_word_list[i]])
    final_word_list.append(next_word)

final = ''
for word in final_word_list:
    final+= str(word) + " "
print(final)
