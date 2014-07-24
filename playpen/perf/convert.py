#!/usr/bin/env

"""
This can be used to produce CSV output based on task times, which can be
imported into spreadsheet software.

The input should be CSV with three columns:
- identifier
- start time as ISO8601
- end time as ISO8601

The output should be CSV with three columns:
- identifier
- start time as seconds since the epoch
- duration in seconds

mongoexport -d pulp_database -c task_status -f start_time,finish_time,result.distributor_type_id \
--query '{task_type: "pulp.server.managers.repo.publish.publish"}' \
--csv | python ./convert.py > publish_perf.csv
"""

import calendar
import csv
import fileinput
import sys

import isodate
    
    
def convert_date_string(datestring):
    as_datetime = isodate.parse_datetime(datestring)
    return calendar.timegm(as_datetime.timetuple())


def main():
    reader = csv.reader(fileinput.input())
    writer = csv.writer(sys.stdout)

    # skip the first row, which has column names
    reader.next()

    for line in reader:
        start, finish, distributor = line
        start_timestamp = convert_date_string(start)
        finish_timestamp = convert_date_string(finish)
        writer.writerow([distributor, start_timestamp, finish_timestamp-start_timestamp])


if __name__ == '__main__':
    main()
