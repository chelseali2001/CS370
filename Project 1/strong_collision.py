import random
import string
from cryptography.hazmat.primitives import hashes

minVal = random.randint(100, 2 ** 22) # Getting a random starting value to test
count = 0
tested = dict()
match = False

print("Strong Collision\n")

# Getting the hash value of each string from the starting value up till 2 ** 23
for x in range(minVal, 2 ** 23):    
    # Getting the hash value
    digest = hashes.Hash(hashes.SHA1())
    digest.update(str(x).encode())
    val = digest.finalize()
    val = list(val)
    test = chr(val[0]) + chr(val[1]) + chr(val[2])
    count += 1

    if count % 250000 == 0:
        print(count, "trials have been tested so far")

    # Checking if the current string's hash value (first 24 bits) was encountered before
    for k,v in tested.items():
        if v == test:
            print("\nString 1:", k)
            print("String 2:", x)
            print("Hash value (first 24 bits in string form):", test)
            print("Number of trials:", count)
            match = True
            break

    # If there's a match in hash value, print the number of trials it took
    # Otherwise, keep track of the hash value from the current string
    if match:
        break
    else:
        tested[x] = test
