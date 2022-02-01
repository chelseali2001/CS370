import random
import string
from cryptography.hazmat.primitives import hashes

minVal = random.randint(100, 2 ** 22) # Getting a random starting value to test
count = 0
match = False

print("Weak Collision\n")

# Testing all string pairs from the starting value up till 2 ** 23
for x in range(minVal, 2 ** 23):
    # Getting the hash value of the string to test
    digest1 = hashes.Hash(hashes.SHA1())
    digest1.update(str(x).encode())
    val1 = digest1.finalize()
    val1 = list(val1)
    string1 = chr(val1[0]) + chr(val1[1]) + chr(val1[2])
    
    # Testing every string within the given range
    for i in range(x + 1, 2 ** 23):
        # Getting the hash value of the second string
        digest2 = hashes.Hash(hashes.SHA1())
        digest2.update(str(i).encode())
        val2 = digest2.finalize()
        val2 = list(val2)
        string2 = chr(val2[0]) + chr(val2[1]) + chr(val2[2])
        count += 1

        # Prints number of trials tested so far (in case program takes too long)
        if count % 250000 == 0:
            print(count, "trials have been tested so far")

        # Checking if the first 24 bits of the hash value for each string matches
        if string1 == string2:
            print("\nString 1:", x)
            print("String 2:", i)
            print("Hash value (first 24 bits in string form):", string2)
            print("Number of trials:", count)
            match = True
            break

    if match:
        break