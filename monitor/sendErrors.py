#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
import os
import sys

if os.stat("/monitor/errors.txt").st_size == 0:
   sys.exit()

errors = open('/var/monitor/errors.txt', 'r+')
msg = MIMEText(errors.read())
msg['Subject'] = 'CA detectMod Script Error'

FROM = 'youremail@domain.com'
recipients = ['recipient@domain.com', 'recipient@domain.com']

msg['From'] = FROM
msg['To'] = " ,".join(recipients)

s= smtplib.SMTP('smtp.gmail.com')
s.starttls()
s.login(FROM, 'yourpassword')
s.sendmail(FROM, recipients, msg.as_string())

errors.truncate(0)
errors.close()
