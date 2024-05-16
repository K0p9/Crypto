import xml.etree.ElementTree as ET

def generate_receipt(xml_file_path, html_file_path):
    # Định nghĩa các định danh namespace
    ns0 = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'
    ns1 = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
    ns2 = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

    # Đọc dữ liệu từ tài liệu XML
    xmlData = ET.parse(xml_file_path)

    # Trích xuất các giá trị tương ứng từ tài liệu XML
    supplierName = xmlData.findtext(f'.//{{{ns2}}}AccountingSupplierParty/{{{ns2}}}Party/{{{ns2}}}PartyName/{{{ns1}}}Name')
    customerName = xmlData.findtext(f'.//{{{ns2}}}AccountingCustomerParty/{{{ns2}}}Party/{{{ns2}}}PartyName/{{{ns1}}}Name')
    lineItems = []
    for item in xmlData.getroot().findall(f'.//{{{ns2}}}InvoiceLine'):
        itemID = item.find(f'.//{{{ns1}}}ID').text
        itemName = item.find(f'.//{{{ns2}}}Item/{{{ns1}}}Name').text
        itemQuantity = item.find(f'.//{{{ns1}}}InvoicedQuantity').text
        itemPrice = item.find(f'.//{{{ns2}}}Price/{{{ns1}}}PriceAmount').attrib['currencyID'] + ' ' + item.find(f'.//{{{ns2}}}Price/{{{ns1}}}PriceAmount').text
        itemTotal = item.find(f'.//{{{ns1}}}LineExtensionAmount').attrib['currencyID'] + ' ' + item.find(f'.//{{{ns1}}}LineExtensionAmount').text
        lineItems.append({
            'id': itemID,
            'name': itemName,
            'quantity': itemQuantity,
            'price': itemPrice,
            'total': itemTotal
        })
    
    # Tạo đoạn mã HTML tương ứng
    htmlContent = f'''
        <h1>Receipt</h1>
        <p>Supplier: {supplierName}</p>
        <p>Customer: {customerName}</p>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
    '''

    for item in lineItems:
        htmlContent += f'''
            <tr>
                <td>{item['id']}</td>
                <td>{item['name']}</td>
                <td>{item['quantity']}</td>
                <td>{item['price']}</td>
                <td>{item['total']}</td>
            </tr>
        '''

    htmlContent += '''
            </tbody>
        </table>
    '''

    # Ghi nội dung HTML vào file receipt.html
    with open(html_file_path, 'w') as f:
        f.write(htmlContent)

def main():
    xml_file_path = input("Enter the XML File Path: ")
    html_file_path = input("Enter the HTML File Path: ")
    generate_receipt(xml_file_path, html_file_path)
    print(f"File '{html_file_path}' has been generated successfully.")

if __name__ == '__main__':
    main()