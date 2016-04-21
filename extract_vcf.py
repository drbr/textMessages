#!/usr/bin/env python
"""
Originally from https://gist.github.com/senko/2692527, I (drbr) have modified
this script to fit my purposes.
"""

"""
Parse phone and email records out of vCard file and store them in a CSV.

Copyright (C) 2012 Senko Rasic <senko.rasic@dobarkod.hr>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import csv
import sys
import string
import logging
import vobject

log = logging.getLogger(__name__)


def sanitize_phone(num):
    """
    Convert phone numbers into standard +<ccode><phonenum> format, without
    spaces, dashes or slashes.
    """

    orig = num
    num = num.translate(None, num.translate(None, string.digits))

    if len(num) <= 10:
        num = '+1' + num
    else:
        num = '+' + num

    if num != orig:
        log.debug('[sanitize_phone] %s -> %s' % (orig, num))
    return num


def parse(fname):
    """
    Parse vCard file. Returns a generator producing dicts with 'name' (string),
    'emails' (list of strings) and 'phones' (list of strings) fields.
    """

    for vobj in vobject.readComponents(open(fname)):
        if not hasattr(vobj, 'fn'):
            log.warning('[parse] skipping entry with no name: ' + repr(vobj))
            continue

        entry = {
            'name': vobj.fn.value.strip(),
            'emails': [],
            'phones': []
        }

        if hasattr(vobj, 'email_list'):
            entry['emails'] = [e.value.strip() for e in vobj.email_list]

        if hasattr(vobj, 'tel_list'):
            entry['phones'] = [sanitize_phone(t.value) for t in vobj.tel_list]

        log.debug('[parse] got entry for ' + entry['name'])

        for phone in entry['phones']:
            yield {
                'name': entry['name'],
                'phone': phone,
                'email': ''
            }

        for email in entry['emails']:
            yield {
                'name': entry['name'],
                'phone': '',
                'email': email
            }


def csv_output(fname, entries):
    """
    Write the entries generated by parse() to a UTF-8 encoded CSV file with
    three columns: Name, Phones and Emails.
    """

    with open(fname, 'wb') as fd:
        writer = csv.writer(fd)
        writer.writerow(['Name', 'Phone', 'Email'])
        for e in entries:
            writer.writerow([
                e['name'].encode('utf-8'), e['phone'], e['email']
            ])


def vcf2csv(infile, outfile):
    """
    Parse entries out of vCard 'infile' and store them to CSV 'outfile'.
    """

    csv_output(outfile, parse(infile))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <infile.vcf> <outfile.csv>" % sys.argv[0]
        sys.exit(-1)
    logging.basicConfig(level=logging.INFO)
    vcf2csv(sys.argv[1], sys.argv[2])