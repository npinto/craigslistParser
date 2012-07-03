#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

# modified from
# http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
class Gmail():

    def __init__(self, gmail_username, gmail_password):
        self.gmail_user = gmail_username 
        self.gmail_pwd = gmail_password 

    def mail(self, to, subject, text, cc = None, attach = None):
       msg = MIMEMultipart()

       msg['From'] = self.gmail_user
       msg['To'] = to
       msg['Subject'] = subject
       if cc is not None:
           msg['CC'] = cc

       msg.attach(MIMEText(text))

       if attach:
           part = MIMEBase('application', 'octet-stream')
           part.set_payload(open(attach, 'rb').read())
           Encoders.encode_base64(part)
           part.add_header('Content-Disposition',
                           'attachment; filename="%s"'
                           % os.path.basename(attach))
           msg.attach(part)

       mailServer = smtplib.SMTP("smtp.gmail.com", 587)
       mailServer.ehlo()
       mailServer.starttls()
       mailServer.ehlo()
       print mailServer.login(self.gmail_user, self.gmail_pwd)
       mailServer.sendmail(self.gmail_user, to, msg.as_string())
       # Should be mailServer.quit(), but that crashes...
       mailServer.close()

if __name__ == "__main__":

    # quick hardcoded cmd line
    import sys
    from pprint import pprint

    fin = open(sys.argv[1])
    fnames = [fname.split()[0] for fname in fin.readlines()]
    txts = [open(fname).read() for fname in fnames]
    emails = [fname.split('__grading.txt')[0].split('/')[-1]
              for fname in fnames]
    pprint(emails)

    # init GMail object with user/pass
    from getpass import getpass
    print "*"*80
    username = raw_input("Gmail account name: ")
    password = getpass("Password: ")
    gm = Gmail(username, password)
    print "*"*80

    cc = "pinto@mit.edu"
    for email, txt in zip(emails, txts):
        to = email # DEBUG: "pinto@mit.edu"
        subject = "CS264 HW4 Grade (%s)" % email
        msg = txt
        attach = None # could be attach = "/path/to/file"
        print email,
        gm.mail(to, subject, msg, cc=cc, attach=attach)
