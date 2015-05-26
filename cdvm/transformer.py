 #!/usr/bin/python
# -*- coding: utf-8 -*-
""" Converter for the cvdm bot """
import sys
import json


def convert_data():
    """ reads the raw data and converts the to
    the simple license schema """
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        raw_record = json.loads(line)

        licence_record = {
            "company_name": raw_record[u'Dénomination'],
            "company_jurisdiction": 'Morocco',
            "source_url": raw_record['source_url'],
            "sample_date": raw_record['sample_date'],
            "jurisdiction_classification": raw_record['type'],
            "category": 'Financial',
            "confidence": 'HIGH',
        }

        if u'Numéro d\'agrément' in raw_record.keys():
            licence_record["licence_number"] = raw_record[u'Numéro d\'agrément']

        print json.dumps(licence_record)

if __name__ == "__main__":
    convert_data()
