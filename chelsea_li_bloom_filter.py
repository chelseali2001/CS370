from cryptography.hazmat.primitives import hashes
import math
import string
import sys
import time

# Generating the hash values
# Negative numbers become positive for this process
def get_hashes(word, hash3, salt):
    if salt: # If salt == 1 or true then use the salt method
        hashList = []
        temp = "00"
        end = 6

        # If hash3 == 1 or true then use 3 hash functions, otherwise use 5 hash functions
        if hash3:
            end = 4

        for x in range(1, end):
            # Salt method: continuously 'n0' to the beginning of the word where n = the number of hash values generated
            # Hash function: SHA-256
            temp += str(x) + "0"
            newWord = temp + word
            digest = hashes.Hash(hashes.SHA256())
            digest.update(newWord.encode())
            val = digest.finalize()
            hashList.append(abs(int(val.hex(), 16)))

        return hashList # Returning the decimal value of each hash value
    elif not salt:
        # Generating hash value with SHA-224
        digest1 = hashes.Hash(hashes.SHA224())
        digest1.update(word.encode())
        val1 = digest1.finalize()
        val1 = abs(int(val1.hex(), 16))
        
        # Generating hash value with SHA-256
        digest2 = hashes.Hash(hashes.SHA256())
        digest2.update(word.encode())
        val2 = digest2.finalize()
        val2 = abs(int(val2.hex(), 16))

        # Generating hash value with SHA-384
        digest3 = hashes.Hash(hashes.SHA384())
        digest3.update(word.encode())
        val3 = digest3.finalize()
        val3 = abs(int(val3.hex(), 16))

        # If hash3 == 1 or true then return the values generated from 3 hash functions
        if hash3:
            return [val1, val2, val3]

        # Generating hash value with SHA-512
        digest4 = hashes.Hash(hashes.SHA512())
        digest4.update(word.encode())
        val4 = digest4.finalize()
        val4 = abs(int(val4.hex(), 16))
        
        # Generating hash value with SHA-512_224
        digest5 = hashes.Hash(hashes.SHA512_224())
        digest5.update(word.encode())
        val5 = digest5.finalize()
        val5 = abs(int(val5.hex(), 16))

        # If hash3 == 0 or false then return the values generated from 5 hash functions
        return [val1, val2, val3, val4, val5]

# Getting the command line arguments
args = sys.argv
dictionary = args[1]
inputFile = args[2]
output3 = args[3]
output5 = args[4]

hash3Time = 0
hash5Time = 0

# Use salt?
salt = int(input("Enter 1 to use the salt method or 0 to use multiple hash functions: "))

while salt != 0 and salt != 1:
    salt = int(input("Error: must enter 1 to use the salt method or 0 to use multiple hash functions: "))

spaces = int(input("Enter 1 to ignore trailing spaces or 0 to consider trailing spaces: "))

# Consider spaces?
while spaces != 0 and spaces != 1:
    spaces = int(input("Error: must enter 1 to ignore trailing spaces or 0 to consider trailing spaces: "))

# Reading all the words from dictionary.txt
f = open(dictionary, 'r')
words = f.read() 
words = words.split("\n")

# Reading in all the passwords
f = open(inputFile, 'r')
passwords = f.read()
passwords = passwords.split("\n")

# Bloom filter size: k = m/n * ln(2)
# k = number of hash functions
# m = bit array/bloom filter size
# n = number of elements inputed from dictionary.txt
bitarr3len = int(3 / math.log(2) * int(len(words)))
bitarr5len = int(5 / math.log(2) * int(len(words)))

bitarr3 = [0] * bitarr3len # Bit array for 3 hash functions
bitarr5 = [0] * bitarr5len # Bit array for 5 hash functions

# Converting every word from dictionary.txt to their respective bit value in the bit array
for x in range(len(words)):
    # Getting the hash values
    hashVals = []

    # Consider spaces?
    if spaces:
        hashVals = get_hashes(words[x].strip(), 0, salt)
    else:
        hashVals = get_hashes(words[x], 0, salt)

    # Collecting the bits for the bit array (3 hash functions)
    bitarr3[hashVals[0] % bitarr3len] = 1
    bitarr3[hashVals[1] % bitarr3len] = 1
    bitarr3[hashVals[2] % bitarr3len] = 1

    # Collecting the bits for the bit array (5 hash functions)
    bitarr5[hashVals[0] % bitarr5len] = 1
    bitarr5[hashVals[1] % bitarr5len] = 1
    bitarr5[hashVals[2] % bitarr5len] = 1
    bitarr5[hashVals[3] % bitarr5len] = 1
    bitarr5[hashVals[4] % bitarr5len] = 1

    # This operation might take a while
    if (x + 1) % 1000 == 0:
        print(str(x + 1), "words processed from the dictionary")

# Write the results for 3 hash functions
f = open(output3, 'w+')

for x in range(1, int(passwords[0])):
    bloomVal = False
    start_time = time.time() # timing the process with 3 hash functions
    values = get_hashes(passwords[x], 1, salt) # Getting the hash values for the passwords

    # If the bit values from all 3 hash functions is set to true in the bit array then the password might be set
    if bitarr3[values[0] % bitarr3len] == 1 and bitarr3[values[1] % bitarr3len] == 1 and bitarr3[values[2] % bitarr3len] == 1:
        bloomVal = True

    hash3Time += time.time() - start_time # stopping the timer

    # Setting the results for the password
    if bloomVal:
        f.write(passwords[x] + " " + "maybe\n")
    else:
        f.write(passwords[x] + " " + "no\n")
    
    # This operation might take a while
    if x % 1000 == 0:
        print(x, "passwords processed with 3 hash functions")

# Write the results for 3 hash functions
f = open(output5, 'w+')

for x in range(1, int(passwords[0])):
    bloomVal = False
    start_time = time.time() # timing the process with 5 hash functions
    values = get_hashes(passwords[x], 0, salt) # Getting the hash values for the passwords

    # If the bit values from all 5 hash functions is set to true in the bit array then the password might be set
    if bitarr5[values[0] % bitarr5len] == 1 and bitarr5[values[1] % bitarr5len] == 1 and bitarr5[values[2] % bitarr5len] == 1 and bitarr5[values[3] % bitarr5len] == 1 and bitarr5[values[4] % bitarr5len] == 1:
        bloomVal = True

    hash5Time += time.time() - start_time # stopping the timer

    # Setting the results for the password
    if bloomVal:
        f.write(passwords[x] + " " + "maybe\n")
    else:
        f.write(passwords[x]+ " " + "no\n")
    
    # This operation might take a while
    if x % 1000 == 0:
        print(x, "passwords processed with 5 hash functions")

# Printing the number of passwords processed
print()
print(len(words), "bad passwords inserted")
print(passwords[0], "bad passwords tested\n")

# Printing the Bloom Filter sizes
print("Bloom Filter size (3 hash functions):", bitarr3len)
print("Bloom Filter size (5 hash functions):", bitarr5len, "\n")

# Getting the average time it takes for the Bloom Filter to check 1 password
hash3Time /= int(passwords[0])
hash5Time /= int(passwords[0])

print("It takes about", hash3Time, "seconds for my Bloom Filter to check 1 password with 3 hash functions.")
print("It takes about", hash5Time, "seconds for my Bloom Filter to check 1 password with 5 hash functions.\n")

# Calculating the probability of getting a false positive
# P = (1-e^(-k*B/N))^k
# P = probability of getting a false positive
# k = number of hash functions
# B = number of bad passwords
# N = Bloom filter size/bit array size
falseP3 = (1 - (math.e ** ((-3 * len(words)) / bitarr3len))) ** 3
falseP5 = (1 - (math.e ** ((-5 * len(words)) / bitarr5len))) ** 5

print("Probability of getting a false positive for 3 hash functions:", falseP3)
print("Probability of getting a false positive for 5 hash functions:", falseP5)