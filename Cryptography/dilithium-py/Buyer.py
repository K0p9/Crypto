import xml.etree.ElementTree as ET
from dilithium import Dilithium2

def verify(public_key_file, xml_file):
    # Load the public key
    with open(public_key_file, 'r') as f:
        pk_hex = f.read()
    pk = bytes.fromhex(pk_hex)

    # Load the XML file and extract the signature value
    tree = ET.parse(xml_file)
    root = tree.getroot()
    signature_element = root.find("signature")
    while signature_element is not None:
        # Extract the signature value and remove the signature element
        signature_value = signature_element.text.strip()
        root.remove(signature_element)
        
        # Get the canonical representation of the XML string
        canonical_xml = ET.tostring(root, encoding="unicode", method="xml")

        # Verify the signature using Dilithium
        try:
            is_valid = Dilithium2.verify(pk, canonical_xml.encode(), bytes.fromhex(signature_value))
            if is_valid:
                print("The signature is valid.")
            else:
                print("The signature is not valid.")
        except Exception as e:
            print("An error occurred while verifying the signature:", str(e))

        # Find the next signature element
        signature_element = root.find("signature")

    # Write the updated XML file
    tree.write(xml_file)




def main():
    public_key_file = input("Enter the path to the public key file: ")
    xml_file = input("Enter the path to the XML file: ")
    verify(public_key_file, xml_file)


if __name__ == "__main__":
    main()