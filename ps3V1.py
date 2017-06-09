# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):

    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	


def get_word_score(word, n):
     
    word=str.lower(word)
    sum_of_point=0
    for letter in word:
        if letter!="*":
            sum_of_point+=SCRABBLE_LETTER_VALUES[letter]
    second_component=7*len(word)-3*(n-len(word))
    if second_component<1:
        second_component=1
    score_of_word=sum_of_point*second_component
    return score_of_word 

def display_hand(hand):
    hand_letter=""
    for letter in hand.keys():
        for j in range(hand[letter]):
             hand_letter+=letter+" "
    return hand_letter      

def deal_hand(n):         
    hand={}
    num_vowels = int(math.ceil(n / 3))-1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n-1):   
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand['*']=hand.get('*', 0) + 1
    return hand


def update_hand(hand, word):
    
    word=str.lower(word)
    new_hand=dict(hand) 
    for letter in word:
        if letter in new_hand: 
            new_hand[letter]-=1
            if new_hand[letter]<1:
                del(new_hand[letter]) 
    return new_hand
    
def is_valid_word(word, hand, word_list):
    
    word=str.lower(word)
    new_word=word
    word_dict=get_frequency_dict(word)
    m=0
    if '*'in word:
        for x in VOWELS:
            new_word=word.replace('*',x)        
            if new_word in word_list:
                for letter in word:
                    if letter in hand and word_dict[letter]<=hand[letter]:                         
                        m+=1                                                   
                    else:
                        return False
                        break
                    if m==len(word):
                        return True
                        break
    else:
        if word not in word_list:
            return False               
        else:
            for letter in word:#h*ney *->o
                if letter in hand and word_dict[letter]<=hand[letter]:#ensure * not count in hand
                    
                        m+=1
                else:
                    return False
                    break
                if m==len(word):
                    return True
        
                
def calculate_handlen(hand):
    length=sum(hand.values())
    return length
 

def play_hand(hand, word_list):       
    total_score=0
    n=sum(hand.values())
    while calculate_handlen(hand)>0:
        print('Current Hand:',display_hand(hand))
        word=input("Enter word, or '!!' to indicate that you are finished:",)
        n=calculate_handlen(hand)
        if is_valid_word(word, hand, word_list)==True:
            total_score+=get_word_score(word, n)
            print(word,'earned',get_word_score(word, n),'points. Total:',total_score,'points')
        elif word=="!!":
            break
        else:
            print("That is not a valid word.")
        hand=update_hand(hand, word)
    if calculate_handlen(hand)==0:
        print('Run out of letters. Total score:',total_score,'points')
    else:
        print('Total score for this hand:',total_score)
    print('-'*20)
    return total_score
        

def substitute_hand(hand, letter):   
    
    new_letter=""
    if letter in hand.keys():#l
        for char in VOWELS+CONSONANTS: 
            if char not in hand.keys():
                new_letter+=char
        new_letter=random.choice(new_letter)
        hand[new_letter]=hand[letter]
        del(hand[letter])   
    return hand
        
    
    
    pass  # TO DO... Remove this line when you implement this function
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    number_of_substitute=1
    number_of_replay=1
    total_score=0
    Hand_left=int(input("Enter total number of hands:"))
    while Hand_left>0:
        hand_size=7    #number of letter in each hand
        hand=deal_hand(hand_size)
        new_hand=dict(hand)
        print("Current hand:",display_hand(hand))                
        if number_of_substitute>0:
            answer_substitute=input("Would you like to substitute a letter?")
            if str.lower(answer_substitute)=='yes':
                letter=input("Which letter would you like to replace:")
                substitute_hand(hand, letter)
                number_of_substitute-=1
        total_score+=play_hand(hand, word_list)
        if number_of_replay>0:
            answer_replay=input("Would you like to replay the hand?")
            if str.lower(answer_replay)=='yes':
                hand=new_hand
                total_score+=play_hand(hand, word_list)
                number_of_substitute-=1
                number_of_replay-=1
        Hand_left-=1
    return total_score
    
    
        
        
    play_hand(hand, word_list)
    
    print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()





