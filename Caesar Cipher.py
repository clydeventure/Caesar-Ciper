# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:23:11 2020

@author: clyde
"""
import random # Used for randomizing the file name and the encryption key.
import string # Used to make character values for the file name.
import json # Used to export and import files.
import os # Used to find if the files exist in the direcotry.

def seperateList(message_raw): # This sperates the user's input into a string of individual characters.
    x = [] # Setting a new list wihtin the function.
    x[:] = message_raw # Saying that we want to create a list from every element in the given string.
    message_raw = x # Setting the input variable equal to the newly split list.
    return message_raw

def markCapitals(message_seperate, capitals_list): # This will sort the string according to whether or not it is a letter, and whether or not it is capitalized.
    for char in range(len(message_seperate)): # For every element in the string:
        # The [0+char] is saying that we want to start with the first element in the list, and move forward one element with each look iteration.
        if message_seperate[0+char].isalpha() == False: # If the element isn't a letter, mark it with a '0'.
            capitals_list.append([message_seperate[0+char], 0]) 
        elif message_seperate[0+char].islower() == True: # If the element is lowercase, mark it with a '1'.
            capitals_list.append([message_seperate[0+char], 1])
        else: # If the element is uppercase, mark it with a '2'.
            capitals_list.append([message_seperate[0+char].lower(), 2]) # Store the previously capitalized letter as a lowercase letter.
    return capitals_list #Return the newly processed string.

def createFileName(): # This will create a random file name.
    x = ( ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))) # This joins together randomly generated strings which include only uppercase letters and numbers.
    # Random.choice wil choose from the choices in the following ().
    return(x)

def encryptMessage(capitals_list, index, file_name):  
    # This function will encode the message by cross referencing the fist element of each nested string in the capitals lists with the index.
    # It will then replace the first element of each nested string with the index of the corresponding letter, or keep it is it is not alpha.
    key = random.randint(1, 99)#This key will be the amount that the letters are shifted. It will be stored as a seperate file and is required to decrypt.
    final_list = []
    for j in range(len(capitals_list)): # For each nested list in the capitals list:
        if capitals_list[j][0].isalpha(): # If the first element is a letter,
            for v, element in enumerate(index): # Cycle through each element of the index and keep track of their index number.
                if element == capitals_list[j][0]: # If the first element in the nested list matches the element in the index,
                    final_list.append([v+key, capitals_list[j][1]]) # Replace the first element in the nested list with the index number of the corresponding letter = the key amount in the index and add it to a new string
        else:
            final_list.append([capitals_list[j][0], capitals_list[j][1]]) # If the element is not a letter, it will be passed over as is.
    with open(f"{file_name}_msg.json", "w") as f: # Write the encrypted message to an external .json file
        json.dump(final_list, f) # json uses dump() to put information into a .json file
    with open(f"{file_name}_key.json", "w") as k: # Write the encryption key to an external .json file
        json.dump(key, k)
    print(f"Success! Your encryption code is {file_name}. (Do not lose this code! You will need it to decrypt your file later.") #Will print your code to decrypt your file later
        
def getEncryptedMessage(index): # This will import your key and message files and decrypt the message for you with the key
    translated_list = [] # Creates a new list of your decrypted letters.
    final_list = [] # We wil now take the nested lists, either capitalize or pass, and create a single list with our message.
    count = 0 # This is for incorrect key input.
    while count < 3: # You have three tried to input the key correctly.
        code_input = str(input("What is the 6 digit code for you encrypted message?: ")) # Input the encryption code you recieved when encrypting originally.
        message_file = (code_input + "_msg.json") # Finds the file name for your message.
        key_file = (code_input + "_key.json") # Finds the file name for your key.
        if os.path.exists(f"{message_file}"): # If the file you input exists, continue.
            break # Will break the loop.
        else: # If the file doesn't exist, you have x amount of tries left.
            count += 1
            print(f"Invalid key. Try again. You have {3 - count} attempt(s) remaining.")
            continue  # Will restart loop
    with open(f"{message_file}", "r") as f: # Imports the json file for your message as a string.
            message_content = json.load(f)
    with open(f"{key_file}", "r") as k: # Imports the json file for your message as an integer.
        key_content = json.load(k)
    for j in range(len(message_content)): # For each nested string
        if isinstance(message_content[j][0], int) == True: # If the first element of the nested string is an integer (meaning that it was originally a letter)
            for x, y in enumerate(index): # For the index number of each element in the index list
                if x == message_content[j][0] -  key_content: # If the index number of the index list matches with the first integer of the nested string minus the encryption key value
                    translated_list.append([y, message_content[j][1]]) # Then replace the integer value with the corresponding element from the index list paired with the capital/lowercase denotation
        else:
            translated_list.append([message_content[j][0], message_content[j][1]]) # If the element in not an integer (a character or number), transcribe it as is
    for a in range(len(translated_list)):
        if translated_list[a][1] == 2: # If the letter was marked with a 2, it must be capitalized.
            q = translated_list[a][0].upper()
            final_list.append(q)
        else:
            final_list.append(translated_list[a][0])
    final_string = ''.join(final_list)
    print("Your message is:\n\n", final_string)
        
capitals_list = [] # This will be the list of nested lists denoting where the elements are letters, and whether they are capitalized or not.
index = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

encrypt_or_decrypt = input("Would you like to encrypt or decrypt a file? (e/d): ")

if isinstance(encrypt_or_decrypt, str) == True and encrypt_or_decrypt.lower() == "e":
    message_raw = input("Write the message you want to encrypt: ")
    message_seperate = seperateList(message_raw) # Gives us our string from the input.
    capitals_list = markCapitals(message_seperate, capitals_list) # Gives us our tagged nested lists.
    file_name = createFileName() # Gives us a random name for our file.
    final_list = encryptMessage(capitals_list, index, file_name) # Encrypts the message and then creates and exports two files: one for the message, one for the key.
elif isinstance(encrypt_or_decrypt, str) == True and encrypt_or_decrypt.lower() == "d":
    open_file = getEncryptedMessage(index)
else:
    print("That is an invalid response")



