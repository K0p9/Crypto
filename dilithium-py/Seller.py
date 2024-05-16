import unittest
import os
import io
from dilithium import Dilithium2
from time import time
from statistics import mean, median
from dilithium import Dilithium
from pymongo import MongoClient
import xml.etree.ElementTree as ET


# XML_content = r'E:\dilithium\dilithium-py\test.xml'
# Connect to the database(MongoDB)
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

    # Sign the canonical XML using Dilithium
    sig = Dilithium2.sign(sk, canonical_xml.encode())

    # save the signature to mongoDB
    db = client["Invoices"]
    collection = db["signed_xml_files"]
    result = collection.insert_one({"xml_file": xml_string, "signature": sig})

    # add signature element to the XML file
    signature_element = ET.SubElement(root, "signature")
    signature_element.text = sig.hex()

    # save the XML file with signature
    xml_with_signature = ET.tostring(root)
    with open(file_path, 'w') as f:
        f.write(xml_with_signature.decode())

    return sig


def main():
    sk = None
    while True:
        print("What do you want to do?")
        print("1. Generate keys")
        print("2. Sign invoice")
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
        elif command == "3":
            break

        else:
            print("Invalid command. Please try again!")

if __name__ == "__main__":
    main()

