# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:23:11 2020

@author: clyde
"""
import random 
import string 
import json 
import os 

def seperate_list(message_raw): 
    # This sperates the user's input into a string of individual characters.
    new_list = [] 
    new_list[:] = message_raw 
    message_raw = new_list
    return message_raw

def mark_capitals(message_seperate, capitals_list): 
    # This will sort the string according to whether or not it is a letter, and whether or not it is capitalized.
    for char in range(len(message_seperate)): 
        if message_seperate[0+char].isalpha() == False: 
            capitals_list.append([message_seperate[0+char], 0]) 
        elif message_seperate[0+char].islower() == True: 
            capitals_list.append([message_seperate[0+char], 1])
        else: 
            capitals_list.append([message_seperate[0+char].lower(), 2]) 
    return capitals_list 

def create_file_name(): 
    # This will create a random file name.
    joined_list = ( ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))) 
    return(joined_list)

def encrypt_message(capitals_list, index, file_name):  
    # This function will encode the message by cross referencing the fist element of each nested string in the capitals lists with the index.
    # It will then replace the first element of each nested string with the index of the corresponding letter, or keep it is it is not alpha.
    key = random.randint(1, 99)
    final_list = []
    for j in range(len(capitals_list)): 
        if capitals_list[j][0].isalpha(): 
            for v, element in enumerate(index):
                if element == capitals_list[j][0]: 
                    final_list.append([v+key, capitals_list[j][1]])
        else:
            final_list.append([capitals_list[j][0], capitals_list[j][1]]) 
    with open(f"{file_name}_msg.json", "w") as f: 
        json.dump(final_list, f) 
    with open(f"{file_name}_key.json", "w") as k: 
        json.dump(key, k)


        
def get_encrypted_message(index): 
    # This will import your key and message files and decrypt the message for you with the key
    translated_list = [] 
    final_list = []
    count = 0 
    while count < 3:
        code_input = str(input("What is the 6 digit code for you encrypted message?: ")) 
        message_file = (code_input + "_msg.json") 
        key_file = (code_input + "_key.json") 
        if os.path.exists(f"{message_file}"): 
            break 
        else:
            count += 1
            print(f"Invalid key. Try again. You have {3 - count} attempt(s) remaining.")
            continue 
    with open(f"{message_file}", "r") as f: 
            message_content = json.load(f)
    with open(f"{key_file}", "r") as k: 
        key_content = json.load(k)
    for j in range(len(message_content)):
        if isinstance(message_content[j][0], int) == True: 
            for x, y in enumerate(index):
                if x == message_content[j][0] -  key_content:
                    translated_list.append([y, message_content[j][1]]) 
        else:
            translated_list.append([message_content[j][0], message_content[j][1]]) 
    for a in range(len(translated_list)):
        if translated_list[a][1] == 2: 
            q = translated_list[a][0].upper()
            final_list.append(q)
        else:
            final_list.append(translated_list[a][0])
    final_string = ''.join(final_list)
    print("Your message is:\n\n", final_string)
        
capitals_list = [] 
index = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

encrypt_or_decrypt = input("Would you like to encrypt or decrypt a file? (e/d): ")

if isinstance(encrypt_or_decrypt, str) == True and encrypt_or_decrypt.lower() == "e":
    message_raw = input("Write the message you want to encrypt: ")
    message_seperate = seperate_list(message_raw) 
    capitals_list = mark_capitals(message_seperate, capitals_list) 
    file_name = create_file_name() 
    final_list = encrypt_message(capitals_list, index, file_name) 
    print(f"Success! Your encryption code is {file_name}. (Do not lose this code! You will need it to decrypt your file later.)")
elif isinstance(encrypt_or_decrypt, str) == True and encrypt_or_decrypt.lower() == "d":
    open_file = get_encrypted_message(index)
    print(f" Your message is: \n\n {open_file}")
else:
    print("That is an invalid response")



