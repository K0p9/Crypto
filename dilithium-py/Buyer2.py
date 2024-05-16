import unittest
import os
import io
from dilithium import Dilithium2
from time import time
from statistics import mean, median
from dilithium import Dilithium
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


# XML_content = r'E:\dilithium\dilithium-py\test.xml'
# Connect to the database(MongoDB)
uri = "mongodb+srv://pttam101203:acop101203@cluster1.1ul9xpw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database_name = "Receipt"
database = client[database_name]

def KEYGEN():
    pk, sk = Dilithium2.keygen()
    pk_hex = pk.hex()
    with open("PublicKey.txt", "w") as f:
        f.write(pk_hex)
    return pk_hex, sk

def SIGN(file_path, sk, client):
    #read the HTML file
    with open(file_path, 'r') as f:
        html_string = f.read()

    # Parse the HTML string and get the root element
    soup = BeautifulSoup(html_string, 'html.parser')

    # Get the canonical representation of the HTML string
    canonical_html = str(soup)

    # Sign the canonical HTML using Dilithium
    sig = Dilithium2.sign(sk, canonical_html.encode())

    # save the signature to MongoDB
    db = client["Receipt"]
    collection = db["signed_receipt_files"]
    result = collection.insert_one({"html_file": html_string, "signature": sig})

    # add signature element to the HTML file
    signature_element = soup.new_tag("signature")
    signature_element.string = sig.hex()

    if soup.body is not None:
        soup.body.append(signature_element)
    elif soup.html is not None:
        soup.html.append(signature_element)
    else:
        soup.append(signature_element)

    # save the HTML file with signature
    html_with_signature = str(soup)
    with open(file_path, 'w') as f:
        f.write(html_with_signature)

    return sig

def main():
    sk = None
    while True:
        print("What do you want to do?")
        print("1. Generate keys")
        print("2. Sign receipt")
        print("3. Quit")

        command = input("> ")

        if command == "1":
            pk, sk = KEYGEN()
            print(f"Public Key: {pk}")
            print(f"Secret Key: {sk}")
            print("=" * 40)

        elif command == "2":
            if not sk:
                print("Please generate keys first!")
            else:
                file_path = input("Enter the file path to sign: ")
                if file_path:
                    signature = SIGN(file_path, sk, client)
                    print(f"Signature: {signature}")
                    print(f"The HTML file at {file_path} has been signed.")
        elif command == "3":
            break

        else:
            print("Invalid command. Please try again!")

if __name__ == "__main__":
    main()
