import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends.openssl.backend import backend

# Make sure there are no trailing whitespaces in the inputs
plaintext = raw_input("Enter the plaintext: ")
ciphertext = raw_input("Enter the ciphertext: ")
print "The IV are all zeros (not the ASCII zero)"

answer = ""
iv = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0' # Setting IV to all zeros

# Reading all of the words in the English word list
with open('words.txt', 'r') as f:
  lines = f.readlines()

# Checking if any of the keys can be used to decrpyt the ciphertext back to the plaintext
for line in lines:
    newline = line.strip() # Getting rid of trailing whitespaces
    
    # If a key is less than 16 characters, add spaces to the end
    while len(newline) < 16:
        newline += " "

    if len(newline) == 16: # Test keys with exactly 16 characters
        key = newline.encode()

        # Decrypting the ciphertext
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend)
        decryptor = cipher.decryptor()
        ct = decryptor.update(ciphertext.decode("hex")) + decryptor.finalize()
        ctList = list(ct) # Convert the message from bytes to a list of ASCII code
        right = True

        # Checking if the deciphered message matches the plaintext (character by character)
        for x in range(len(plaintext)):
            if ctList[x] != plaintext[x]:
                right = False
                break
        
        # Checking if the right key is found
        if right:
            answer = key
            break

print"The key is", str(answer) # Printing out the key in string form