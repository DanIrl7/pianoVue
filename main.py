def letters(word):
    letter_count = {}
 

    for letter in word:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
    
    return letter_count

def anagram(word1, word2):
    print(letters(word1) == letters(word2))

# anagram('restful', 'restiiul')
greeting = input()

print(greeting.index("h"))
