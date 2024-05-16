from bs4 import BeautifulSoup
from dilithium import Dilithium2

def verify(public_key_file, html_file):
    # Load the public key
    with open(public_key_file, 'r') as f:
        pk_hex = f.read()
    pk = bytearray.fromhex(pk_hex)

    # Load the HTML file and extract the signature value
    with open(html_file, 'r') as f:
        html_string = f.read()
    soup = BeautifulSoup(html_string, 'html.parser')
    signature_element = soup.find("signature")
    while signature_element is not None:
        # Extract the signature value and remove the signature element
        signature_value = signature_element.string.strip()
        signature_element.extract()

        # Get the canonical representation of the HTML string
        canonical_html = str(soup)

        # Verify the signature using Dilithium
        try:
            is_valid = Dilithium2.verify(pk, canonical_html.encode(), bytes.fromhex(signature_value))
            if is_valid:
                print("The signature is valid.")
            else:
                print("The signature is not valid.")
        except Exception as e:
            print("An error occurred while verifying the signature:", str(e))

        # Find the next signature element
        signature_element = soup.find("signature")

    # Write the updated HTML file
    with open(html_file, 'w') as f:
        f.write(str(soup))


def main():
    public_key_file = input("Enter the path to the public key file: ")
    html_file = input("Enter the path to the HTML file: ")
    verify(public_key_file, html_file)


if __name__ == "__main__":
    main()