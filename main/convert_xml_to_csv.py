import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import argparse
import csv
import os
import re 
path = '../000000217816000070_proxy-t13.xml'

os_path = '../test_data_labels/'
csv_save_path = '../csv_data/'

def remove_empty_columns(table_data):
    length = min(len(row) for row in table_data)
    # Iterate over each position in the list
    for i in range(length):
        # Get the values at the current position from all lists
        values = [row[i] for row in table_data]
        # Check if all values at this position are null
        if all(value == '' for value in values):
            # If all values are null, remove them from all lists
            for row in table-data:
                del row[i]
    return table_data

def parse_xml(xml_file):
    tree = ET.parse(f"{os_path}{xml_file}")
    root = tree.getroot() 
    root_str = ET.tostring(root, encoding='unicode')
    root_str = "<html>" + root_str + "</html>"

    soup = BeautifulSoup(root_str, 'xml')

    # Find the <object> element
    object_element = soup.find('object')

    # Find the <html> element within <object>
    html_element = object_element.find('html') if object_element else None

    # Check if <html> element exists
    if html_element:
        # Find the <table> element within <html>
        table_element = html_element.find('table')
        previous_value = '' 
        # Extract table data
        if table_element:
            table_data = []
            for row in table_element.find_all('tr'):
                row_data = []
                for cell in row.find_all(['td', 'th']):
                    cell_value = cell.get_text(strip=True)
                    row = re.findall(r'rowspan="[0-255]"', str(cell))
                    col = re.findall(r'colspan="[0-255]"', str(cell))
                    if previous_value == "$":
                        cell_value = '$' + cell_value
                    elif previous_value == "%":
                        cell_value = cell_value + '%'
                    if cell_value == '$':
                        cell_value = ''
                        previous_value = '$'
                    elif cell_value == "%":
                        cell_value = ''
                        previous_value = '%'
                    else:
                        previous_value = ''
        
                    if "colspan" in str(col):
                        row_data.append('')
                    row_data.append(cell_value)
                table_data.append(row_data)
            try: 
                table_data = remove_empty_columns(table_data)
            except:
                print(table_data)
                print('*****')
                print(f"Error formatting the CSV file {xml_file}")
                import ipdb; ipdb.set_trace()
            # Write table data to CSV file
            with open(f'{csv_save_path}{xml_file.split(".")[0]}.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(table_data)
        
        else:
            print("<table> element not found.")
    else:
        print("<html> element not found.")

def main_file():
    files = os.listdir(os_path)
    for file in files:
        parse_xml(file)
if __name__ == "__main__":
    main_file()    


,,,,Annual....