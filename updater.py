#!/usr/bin/python

"""
Craigslist RSS poller.
Copyright (c) 2011. Jake Brukhman <jbrukh@gmail.com>. See LICENSE.
Modified April 2012 by Pat O'Keefe <patokeefe1@gmail.com>
"""

import craigslist
import optparse
import time
import sys
import smtplib
import conf
from string import Template

class LookupQueue(object):
    """A bounded queue backed by a set for fast membership lookup and which does not accept
    duplicate elements.

    4/2012 -- Acceptable posts now need to contain a keyword from the configuration
    file.
    """

    def __init__(self, size):
        self.s = set()
        self.q = []
        self.size = size

    def push(self, *items):
        for item in items:
            if item['link'] not in self.s:
                if self.containsKeyword(item):
                    if len(self.q) == self.size:
                        self.pop()
                    self.s.add(item['link'])
                    self.q.append(item['link'])
                    return item


    def containsKeyword(self, item):
        postTitle = item['title'].lower()
        for k in conf.KEYWORDS:
            if k in postTitle:
                # print "Pushed to queue because ", postTitle, " contains ", k
                return True
        return False


    def pop(self):
        item = self.q.pop(0)
        self.s.remove(item)
        return item

    def __contains__(self, item):
        return item in self.s

    def __len__(self):
        return len(self.q)

    def __str__(self):
        return self.q.__str__()

    def __repr__(self):
        return self.q.__str__()




def main(opts):
    """
    Indefinitely cycles through the queries provided to the program,
    and extracts the new apartment information.

    """

    # The query URL now comes from the conf.py file. I rarely need to change it, and
    # didn't want to have to chase it down if it somehow left my bash history.
    query = conf.CRAIGS_URL

    queue = LookupQueue(opts.memory)

    while True:
        listings = craigslist.fetch_with_pages_back(query, pages=opts.pages)
        new_listings = [l for l in listings if queue.push(l)]

        # # If you just want to print out the relevant posts...
        # for listing in new_listings:
        #     print Template(opts.format).safe_substitute(listing)

        # Attempt to send an email containing the new posts
        if len(new_listings) > 0:
            msg = get_msg(new_listings, query)
            print msg
            try:
                send_email(conf.SENDER, conf.RECIPIENTS.split(';'), msg)
            except:
                print "Could not send email: ", sys.exc_info()[0]

        process_new(new_listings)
        time.sleep(opts.sleep)




def process_new(listings):
    pass


def get_msg( new_listings, query ):
    """Create the listing summary email. Don't forget to add the relevant information into
    conf.py
    """
    subject = "%d New Apartments to Investigate" % (len(new_listings))
    header = "From: %s\nTo: %s\nSubject: %s\n\n" % (conf.SENDER, conf.RECIPIENTS, subject)
    body = header+"\n\n".join(["%(date)s %(title)s\n%(link)s"%(item) for item in new_listings])
    return body


def send_email( sender, recipients, msg ):
    """Send the email. Don't forget to add the relevant information into conf.py
    """

    from gmail import Gmail
    gm = Gmail(conf.SMTP_USER, conf.SMTP_PASS)
    print recipients
    gm.mail(recipients[0], 'alert palo alto', msg[:100])
    gm.mail(recipients[1], 'alert palo alto', msg)
    return

    session = smtplib.SMTP(conf.SMTP_SERVER)
    session.starttls()
    session.login(conf.SMTP_USER, conf.SMTP_PASS)
    smtpresult = session.sendmail(sender, recipients, msg)

    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not delivery mail to: %s

  Server said: %s
  %s

  %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        raise smtplib.SMTPException, errstr


if __name__ == '__main__':
    USAGE = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-m', '--memory', dest='memory', type='int', default=1000,
            help='number of historical items against which to test for uniqueness (set high)')
    parser.add_option('-s', '--sleep', dest='sleep', type='int', default=30,
            help='polling period, in seconds')
    parser.add_option('-f', '--format', dest='format', default='${date}\t${title}', type='string',
            help="output format, using Python formatting; available fields are ['date', 'title', 'link'] and \
			the default format is '${date}\\t${title}'")
    parser.add_option('-p', '--pages', dest='pages', default=1, type='int',
            help="the number of pages back from this url, if possible, up to 10")

    (opts, args) = parser.parse_args()

    # init GMail object with user/pass
    from getpass import getpass
    from os import environ
    print "*"*80
    username = environ.get('CL_U', None)
    if username is None:
        username = raw_input("Gmail account name: ")
    password = environ.get('CL_P', None)
    if password is None:
        password = getpass("Password: ")
    conf.SMTP_USER = username
    conf.SMTP_PASS = password
    print "*"*80

    if opts.pages<0 or opts.pages>10:
        print "Ten pages back maximum."
        sys.exit(1)

    try:
        main(opts)
    except KeyboardInterrupt:
        print "Goodbye!"
