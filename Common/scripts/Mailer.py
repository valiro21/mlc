# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import os
import json
import smtplib


def send_email(recipient, subject, body, current_user):
    init_file = os.path.join(os.path.dirname(__file__), 'mail_config.json')
    with open(init_file, "r") as mail_config:
        config = json.load(mail_config)
        gmail_user = config['gmail_user']
        gmail_pwd = config['gmail_pwd']
    body = "Hello " + current_user + ",\n" + body
    FROM = "MLC Team <hello@mlc.com>"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail to %s' % TO)
        return 0
    except:
        print("failed to send mail for email %s" % TO)
        return -1
