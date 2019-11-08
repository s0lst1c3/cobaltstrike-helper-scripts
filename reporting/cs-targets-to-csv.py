#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup

def setup():

    parser = argparse.ArgumentParser()

    parser.add_argument('--input-file', '-i',
                        dest='input_file',
                        type=str,
                        required=True,
                        help='Specify path to input file (XML from CS)')

    parser.add_argument('--output-file', '-o',
                        dest='output_file',
                        type=str,
                        required=True,
                        help='Specify path to output file (CSV)')

    parser.add_argument('--unique', '-u',
                        dest='unique',
                        action='store_true',
                        help='Remove duplicates.')

    parser.add_argument('--sort-by', '-s',
                        dest='sort_by',
                        default='address',
                        type=str,
                        choices=['address', 'name', 'os'],
                        help='Sort entries by specified column.')

    args = parser.parse_args()

    return args

def reader(input_file):

    with open(input_file) as input_handle:
        raw_xml = input_handle.read()
    soup = BeautifulSoup(raw_xml)
    
    for entry in soup.findAll('entry'):

        print(entry)
        next_entry = {}
        
        for address in entry.findAll('address'):
            next_entry['address'] = address.text

        for name in entry.findAll('name'):
            next_entry['name'] = name.text

        next_entry['os'] = []
        for os in entry.findAll('os'):
            next_entry['os'].append(os.text)
        for os in entry.findAll('version'):
            next_entry['os'].append(os.text)
        next_entry['os'] = ' '.join(next_entry['os'])

        yield next_entry
    
def entry2line(entry):

    return ','.join([entry['address'],
                entry['name'],
                entry['os']])

def main():

    args = setup()

    sort_by = args.sort_by
    input_file = args.input_file
    output_file = args.output_file
    unique = args.unique
    
    lines = set([])

    with open(output_file, 'w') as output_handle:
        output_handle.write('address,name,os\n')
        for entry in sorted(reader(input_file), key=lambda i: i[sort_by]):

            next_line = entry2line(entry)
            if unique and next_line in lines:
                continue
            else:
                lines.add(next_line)
            output_handle.write('{}\n'.format(next_line))
        
if __name__ == '__main__':
    main()
