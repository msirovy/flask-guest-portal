# -*- coding: utf-8 -*-

import yaml
import subprocess
import pymysql
import smtplib
from jinja2 import Template
from email.mime.text import MIMEText


def load_yaml(file_path):
    """ Load yaml file as dict
    """
    try:
        with open(file_path, 'r') as F:
            return yaml.load(F)
    except ImportError:
        print("import yaml is required")
        exit(1)


def send_mail(smtp, template, data):
    """ Send email
        ----------
        assamble email from template and given data,
        than send it to garant_mail address

        smtp=dict(
            server=     str() smtp server ip or hostname
            login=      str() smtp login
            password=   str() smtp password
            sender=     str() email address of sender
            )
        template=       str() path to file with email template
        data=dict(
            garant_mail=str() email of recipient (allow access to guest)
            first_name= str() applicant first name
            last_name=  str() applicant last name
            ...         you can add more depend on template
                        and enroll form in forms.py
        )
    """

    # load template from file
    try:
        with open(template, 'r', encoding="utf-8") as TPL:
            tpl = Template(TPL.read())

    except IOError as err:
        print(err)
        exit(1)

    msg = MIMEText(tpl.render(**data), 'plain', _charset='utf-8')
    msg['MIME-Version:'] = "1.0"
    msg['To'] = data['garant_mail']
    msg['From'] = smtp['sender']
    msg['Subject'] = 'FZU-GUEST {first_name} {last_name}'.format_map(data)
    msg["Content-Type"] = "text/plain;charset=UTF-8;format=flowed"
    msg["Content-Transfer-Encoding"] = '8bit'
    msg['X-Sender'] = smtp['sender']
    # debug print(msg.as_string())

    try:
        server = smtplib.SMTP(smtp['server'])
        server.starttls()
        server.login(smtp['login'], smtp['password'])
        server.sendmail(smtp['sender'], data['garant_mail'], msg.as_string())
        return True

    except IOError as err:
        print("Server unavaliable: ", err)
        return False


def db_exec(db, query=None, debug=False):
    """ Encapsulate database request to function
        to keep flexibility of this script.
        db=dict(
            host=   str() ip address or hostname to db server
            user=   str() login name to database
            passwd= str() login passwword to database
            db=     str() database name
            )
        query=str()
    """
    con = False

    try:
        con = pymysql.connect(
                        host=db['server'],
                        user=db['login'],
                        passwd=db['password'],
                        db=db['db']
                    )
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        return [line for line in cursor]

    except pymysql.Error as err:
        if debug:
            print(err)
        return False

    finally:
        if con:
            cursor.close()
            con.close()


def get_mac(ipaddress):
    """ Call get_arp.sh script that return mac address for given ip
    """
    try:
        return subprocess.check_output([
                    "/home/enroll/enroll/get_arp.sh",
                    ipaddress
                ]).decode('utf-8')

    except IOError as err:
        print(err)
        return False


def str2mac(mac):
    """ Convert mac in format 00aa11bb33 to 00:aa:11:bb:33
    """
    return ":".join([
            str(mac[a] + mac[a+1]) for a in range(0, len(mac), 2)
        ])


def valid_grant(smtp, username, password):
    """ Try grant's given username and password for login
        to smtp server to be able grant is authorized and real
        person (everybody who has mail account was been authorized
        and have personal id)
    """
    try:
        server = smtplib.SMTP(smtp['server'])
        if server.login(username, password):
            return True
        else:
            return False
    except TimeoutError:
        return False
