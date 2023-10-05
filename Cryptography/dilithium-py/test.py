import unittest
import os
import io
from dilithium import Dilithium2
from time import time
from statistics import mean, median
from dilithium import Dilithium
from pymongo import MongoClient
import xml.etree.ElementTree as ET



##XML_content = r'E:\dilithium\dilithium-py\test.xml'
#Connect to the database(MongoDB)
uri = "mongodb+srv://pttam101203:acop101203@cluster1.1ul9xpw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database_name = "Invoices"
database = client[database_name]

def KEYGEN():
    pk, sk = Dilithium2.keygen()
    pk_hex = pk.hex()
    with open("PublicKey.txt", "w") as f:
       f.write(pk_hex)
    return pk_hex, sk
              
def SIGN(file_path, sk, client):
    #read the XML file
    with open(file_path, 'r') as f:
       xml_string = f.read()

    # Parse the XML string and get the root element
    root = ET.fromstring(xml_string)

    # Get the canonical representation of the XML string
    canonical_xml = ET.tostring(root, encoding="unicode", method="xml")

    #Sign the canonical XML using Diilithium
    sig = Dilithium2.sign(sk, canonical_xml.encode())

    #save the signature to mongoDB
    db = client["Invoices"]
    collection = db["signed_xml_files"]
    result = collection.insert_one({"xml_file": xml_string, "signature": sig})

    #save the signature to a text file
    sig_hex = sig.hex()
    with open('signature.txt', 'w') as f:
        f.write(sig_hex)


    return sig

def VERIFY(xml_file, signature_file, publickey_file):
    # Read the XML file
    with open(xml_file, 'r') as f:
        xml_string = f.read()

    # Parse the XML string and get the root element
    root = ET.fromstring(xml_string)

    # Get the canonical representation of the XML string
    canonical_xml = ET.tostring(root, encoding="unicode", method="xml")

    # Read the signature from file
    with open(signature_file, 'r') as f:
        signature_hex = f.read()

    # Convert the signature from hex to bytes
    signature = bytes.fromhex(signature_hex)
    
    #Mở file PublicKey.txt
    with open(publickey_file, 'r') as f:
        publickey_hex = f.read()

    # Convert the public key from hex to bytes
    pk = bytes.fromhex(publickey_hex)

    # Verify the signature using Dilithium
    is_valid = Dilithium2.verify(pk, canonical_xml.encode(), signature)

    # Compare the original XML string and the canonical one
    original_xml = ET.tostring(root, encoding="unicode", method="xml")
    is_same = original_xml == canonical_xml

    # Print the verification result and the comparison result
    print("Signature is valid:", is_valid)
    print("XML is same before and after signing:", is_same)


def main():
    while True: 
        print("What do you want to do?")
        print("1. Generate the keys")
        print("2. Sign the invoice")
        print("3. Verify the signature")
        print("4. Quit")
        command = input()

        if command == "1":
            pk_hex, sk = KEYGEN()
            print("Here is your Public Key: ", pk_hex)
            print("\n")
            print("Here is your Secret Key: ", sk)
            print("=========================================")

        elif command == "2":
            file_path = input("Enter the file path to sign: ")
            if file_path:
                signature = SIGN(file_path, sk, client)
                with open('signature.txt', 'w') as f:
                    f.write(signature.hex())
                print("Here is the signature: ", signature)

        elif command == "3":
            xml_file = input("Enter the path to the XML file: ")
            signature_file = input("Enter the path to the signature file: ")
            publickey_file = input("Enter the path to the PublicKey file: ")
            if xml_file and signature_file and publickey_file:
                VERIFY(xml_file, signature_file, publickey_file)

        elif command == "4":
            break

        else:
            print("Invalid command. Please try again!")

main()