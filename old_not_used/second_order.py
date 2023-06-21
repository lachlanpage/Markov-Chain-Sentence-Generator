#Markov Model Second Order Sentence Generator 
#By Lachlan Page
import random 

file_string = ""
with open("bleak-house.txt", 'r') as content_file:
    file_string = content_file.read()

#Fixing formatting for sampletext, this can be removed for other training_corpus_filename sources
file_string = file_string.lower()
file_string = file_string.replace("!" , " ")
file_string = file_string.replace("." , " ")
file_string = file_string.replace("," , " ")
file_string = file_string.replace("@" , " ")
file_string = file_string.replace("&amp;", " ")
file_string = file_string.replace("?", " ")
file_string = file_string.replace("-", " ")
file_string = file_string.split()

#full stop in dictionary to handle end cases
chain = {}
chain['.'] = ' '

#More efficient algorith. O(n)
for i in range(0, len(file_string)):
    if(i + 1 < len(file_string)):
        key = (file_string[i], file_string[i+1])
        if key not in chain: 
            chain[key] = []
            if(i+2 < len(file_string)):
                chain[key].append(file_string[i+2])
            else:
                chain[key].append('.')
        else:
            #already exists in chain
            if(i+2 < len(file_string)): 
                chain[key].append(file_string[i+2])
            else:
                chain[key].append('.')

#prediction
WORD_LENGTH = 6
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
