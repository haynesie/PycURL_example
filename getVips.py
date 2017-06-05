#! /usr/bin/env python

import pycurl
from StringIO import StringIO
import json
import re

public_vips = []

def get_vips():
    '''
        This function pulls a list of deployed virtual IP addresses from 
        the database via an API call and syphons-off special cases. 
    '''

    buffer = StringIO()
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'https://somedatabase.com/api')
        c.setopt(pycurl.VERBOSE, 0)
        c.setopt(pycurl.USERPWD, 'usern:passwd')
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close
    except pycurl.error, error:
        errno, errstr = error
        print  "Couldn't connect to database server!!  error: ", errno, " ", errstr
        return

    vips = buffer.getvalue()
    json.loads(vips)
    ips = json.loads(vips)

    all_vips = [(vip['ip'], vip['name']) for vip in ips]

    for item in all_vips:
        result1 = re.match("^10\.*", item[0])
        result2 = re.match("^us[0-9]+\.", item[1])
        if result1 or result2:
            continue
        else:
            public_vips.append(item)

def main():
    get_vips()
    for vip in public_vips:
        print str(vip[0]) + ":" + str(vip[1])

if __name__ == '__main__':
    main()

