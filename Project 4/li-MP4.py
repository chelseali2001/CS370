import pyqrcode
from pyqrcode import QRCode
import sys
import time
import hmac
import base64
import struct
import hashlib

# Dynamic Truncation
def DT(HS):
    # Getting the low-order 4 bits of the last byte of the hash value
    # Then converting the bits to int
    Offset = HS[19] & 15

    P = struct.unpack(">I", HS[Offset : Offset + 4])[0] # Getting the int value of the bytes between Offset-(Offset + 4) in the hash value
    P = P & 0x7fffffff # Getting the last 31 bits of it
    
    return P

# Getting the command line argument
args = sys.argv
mode = args[1]

if mode == "--generate-qr": # Making the qr code
    s = "otpauth://totp/"   # Specifying the type
    label = "OSU:student@oregonstate.edu?" # Label
    secret = "secret=JBSWY3DPEHPK3PXP&" # Secret key
    issuer = "issuer=OSU&" # Issuer
    algorithm = "algorithm=SHA1&" # Algorithm being used
    digits = "digits=6&" # Number of digits for otp
    period = "period=30" # Period of time otp will be valid for

    # Putting everything together for the key uri format
    s += label + secret + issuer + algorithm + digits + period

    # Print the key uri
    print(s)

    # Generate QR code
    url = pyqrcode.create(s)
    
    # Create and save the svg file naming "myqr.svg"
    url.svg("myqr.svg", scale = 8)
elif mode == "--get-otp": # Making the otp
    secret = b'JBSWY3DPEHPK3PXP' # The key being used (borrowed from the qr code generator)
    key = base64.b32decode(secret, True) 
    X = 30 # Setting the period of time the otp will be valid
    T = int(time.time() // X) # Getting the current unix time

    while True: # This process will go on forever until the user stops the program
        # Generating an HMAC-SHA-1 value
        msg = struct.pack(">Q", T)
        HS = hmac.new(key, msg, hashlib.sha1).digest()

        # Generating a 4-byte string
        Sbits = DT(HS) 

        # Compute a TOTP value
        d = Sbits % (10 ** 6) # 10 ** 6 is used to make a 6 digit otp

        sd = ""

        # If the number is less than 6 digits (int values don't include 0 at the beginning of the number)
        # then add 0 to the head of the password till it makes a 6 digit number
        if len(str(d)) < 6:
            for x in range(6 - len(str(d))):
                sd += "0"

            sd += str(d)
        else:
            sd = str(d)

        # Printing otp
        print(sd)

        count = T

        # Collecting the new counter after 30 seconds
        while T == count:
            T = int(time.time() // X)
