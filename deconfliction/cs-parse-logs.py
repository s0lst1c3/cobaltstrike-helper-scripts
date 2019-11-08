#!/usr/bin/env python3

import glob
import os
import json

log_dir = '/path/to/cs/log/dir/here'
filter_by_date = '12/12'
user_filter = ''

subdirs = os.listdir()

def get_log_entries():

    for date_dir in subdirs:

        if 'script.py' in date_dir or '.txt' in date_dir:
            continue

        for host_dir in os.listdir(date_dir):

            if 'events.log' in host_dir:
                continue

            for log_file in glob.glob('{}/{}/*.log'.format(date_dir, host_dir)):

                with open(os.path.join(log_file)) as fd:
                    for line in fd:
                        line = line.strip()
                        if user_filter in line and 'input' in line and filter_by_date in line:

                            datestamp = line[:line.index('[')].strip()
                            command = line[line.index('>')+1:].strip()
                            host = host_dir.strip()

                            yield {
                                'datestamp' : datestamp,
                                'host' : host,
                                'command' : command,
                            }

if __name__ == '__main__':

    for entry in sorted(get_log_entries(), key=lambda e: e['datestamp']):

        print(entry['datestamp'])
        print(entry['host'])
        print(entry['command'])
        print()
        print()
