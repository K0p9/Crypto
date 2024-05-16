import unittest
import os
import io
from dilithium import Dilithium2
from time import time
from statistics import mean, median
from dilithium import Dilithium
from pymongo import MongoClient
import xml.etree.ElementTree as ET

def verify(public_key_file, signature_file, xml_file):
    # Get the public key from the file
    with open(public_key_file, 'r') as f:
        pk_hex = f.read()

    #Convert the Public Key from hex to bytes
    pk = bytes.fromhex(pk_hex)

    # Get the signature from the file
    with open(signature_file, 'r') as f:
        sig_hex = f.read()

    # Convert the signature from hex to bytes
    sig = bytes.fromhex(sig_hex)

    #Convert the Publickey from hex to bytes

    # Read the XML file
    with open(xml_file, 'r') as f:
        xml_string = f.read()

    # Parse the XML string and get the root element
    root = ET.fromstring(xml_string)

    # Get the canonical representation of the XML string
    canonical_xml = ET.tostring(root, encoding="unicode", method="xml")
    # Verify the signature using Dilithium
    try:
        result = Dilithium2.verify(pk, canonical_xml.encode(), sig)
        if result:
                print("The signature is valid.")
        else:
                print("The signature is not valid.")
    except: 
        print("An error occurred while verifying the signature.")


def main():
    print("Enter the path to the public key file:")
    public_key_file = input()
    print("Enter the path to the signature file:")
    signature_file = input()
    print("Enter the path to the XML file:")
    xml_file = input()
    verify(public_key_file, signature_file, xml_file)






main()