#! /usr/bin/env python

import pycurl
from StringIO import StringIO
import json
import re
import sys

def get_status(vip):

    ''' 
        This function makes a http connection to a server using 
        a virtual IP and retains the HTTP return code. This
        return code is then later used to determine whether to 
        signal an alert. 
    '''
    address = str(vip[0])
    hoststuff = "host: " + str(vip[1])
    header = [hoststuff]
    buffer = StringIO()
    try:
        thisvip = pycurl.Curl()
        thisvip.setopt(pycurl.URL, address)
        thisvip.setopt(pycurl.HTTPHEADER, header)
        thisvip.setopt(pycurl.VERBOSE, 0)
        thisvip.setopt(pycurl.CONNECTTIMEOUT, 10)
        thisvip.setopt(thisvip.WRITEDATA, buffer)
        thisvip.perform()
    except pycurl.error, error:
        errno, errstr = error
        #print address, ' error: ', errno, " ", errstr
        return 1000
    thisvip.close
    return thisvip.getinfo(pycurl.HTTP_CODE)

def main():
    ipaddr, vhostname = sys.argv[1:]
    vip = [ipaddr, vhostname]
    status = get_status(vip)
    print status
    if status < 399:
        return 0
    else:
        return status

if __name__ == '__main__':
    main()
