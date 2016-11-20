#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request
import hashlib
import time
from os import path
from forms import Enroll, Enroll_cz, Login
from lib import load_yaml, db_exec, str2mac, get_mac
from lib import valid_grant, send_mail


app = Flask(__name__)
app.debug = True
app.secret_key = "PLEASE_INPUT_REALY_SECURE_KEY_987221"


CUR_DIR = path.abspath(path.curdir)
CONF = load_yaml(path.join(CUR_DIR, 'settings.yml'))
db = CONF['database']
smtp = CONF['smtp']


@app.route("/", methods=['GET', 'POST'])
@app.route("/<lang>", methods=['GET', 'POST'])
def register(lang="cs"):
    if lang == 'cs':
        _form = Enroll_cz(request.form)
        msg_mail = "Zpráva byla odeslána vašemu ručiteli. " + \
            "Jakmile potvrdí vámi zaslaný email, budete moci " + \
            "využívat síť <strong>FZU-GUEST</strong>."

    else:
        _form = Enroll(request.form)
        msg_mail = "Message has sent to your garant. " + \
            "After garant confirm that mail you will be able " + \
            "to use <strong>FZU-GUEST</strong> network."

    try:
        if request.method == 'POST' and _form.validate():
            _data = {k: str(v) for k, v in _form.data.items()}
            _data['mac_addr'] = get_mac(request.remote_addr)
            _data['table_name'] = db['table']

            md5 = hashlib.md5()
            hash_str = str(_data['mac_addr'] +
                           _data['garant_mail'] +
                           str(time.time()))
            md5.update(hash_str.encode())

            _data['code_reg'] = md5.hexdigest()
            _data['mac_addr'] = get_mac(request.remote_addr)

            sql = "INSERT INTO {table_name} " + \
                        "(code_registration, " + \
                            "first_name, " + \
                            "last_name, " + \
                            "phone, " + \
                            "mail, " + \
                            "days, " + \
                            "garant_mail, " + \
                            "mac_addr) " + \
                        "VALUES (" + \
                            "'{code_reg}', " + \
                            "'{first_name}', " + \
                            "'{last_name}', " + \
                            "'{phone}', " + \
                            "'{mail}', " + \
                            "'{days}', " + \
                            "'{garant_mail}', " + \
                            " '{mac_addr}');".format_map(_data)

            """ send email to grant, save request to db
                and show enroll page
            """
            if send_mail(smtp=smtp,
                         template=CONF['confirm_mail'], data=_data):
                db_exec(db, sql, debug=True)
                return render_template(
                                    'layout.j2',
                                    message=msg_mail
                                )

        else:
            return render_template(
                            'enroll.j2',
                            form=_form,
                            lang=lang,
                        )

    except KeyError as err:
        return render_template(
                        'enroll.j2',
                        form=_form,
                        lang=lang,
                    )


@app.route("/confirm/<code_registration>", methods=['POST', 'GET'])
def confirm(code_registration=None):
    form = Login(request.form)
    _data = db_exec(
            db,
            "select * from enroll where code_registration = '{}'".format(
                code_registration
            ), debug=True)[0]

    msg = "<p>Uživatel je povolen, během 10ti minut mu zřídíme " + \
        "přístup do sítě FZU-GUEST.</p> <hr noshade>" + \
        "<p>User has approved, access to FZU-GUEST" + \
        " will be set during 10 minutes.</p>"

    if request.method == 'POST' and form.validate():
        if valid_grant(smtp, form.username.data, form.password.data):
            db_exec(
                db,
                "update enroll "
                "SET date_confirm = '{date_now}' "
                "where code_registration =  '{code_registration}'"
                "".format(
                        date_now=time.strftime("%Y-%m-%d"),
                        code_registration=code_registration
                    )
            )

        return render_template(
                        'layout.j2',
                        message=msg,
                    )

    else:
        return render_template(
                        'confirm.j2',
                        data=_data,
                        form=Login(request.form),
                    )


@app.errorhandler(404)
def error(error):
    return redirect('/')


@app.route("/get")
def get(locality=None):
    """URL where iptables firewall request mac address
    """
    sql = "select mac_addr from enroll where " + \
        "DATE_ADD(date_confirm, INTERVAL " + \
        "days DAY) > '%s';" % time.strftime("%Y-%m-%d")
    _ret = ""
    for line in db_exec(db, sql, debug=True):
        _ret += str2mac(line['mac_addr']) + "\n"
    return _ret


if __name__ == '__main__':
    app.run(host=CONF['host'], port=5000)
