# -*- coding: utf-8 -*-
#
# ToDo: Better lang-support, this hotfix is not good
#

from wtforms import Form, validators, TextField, SelectField, PasswordField


class Enroll(Form):
    language = SelectField('Language',
                    choices=[
                        ("cs", "CZ Česky"),
                        ("en", "EN English")],
                    default="en"
                )

    first_name = TextField('First name', [
                    validators.Required(
                        message="First name is required.")
                ])

    last_name = TextField('Last name', [
                    validators.Required(
                        message = "Last name is required.")
                ])

    phone = TextField('Phone', [
                validators.regexp(
                    '^(\+420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$',
                    message="Valid formats are: <ul>" +
                            "<li> +420 123 123 123</li>" +
                            "<li> 123 123 123</li>" +
                            "<li>123123123</li>" +
                            "</ul>")
                ])

    mail = TextField('E-mail', [
                validators.Regexp(
                    '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$',
                    message="Correct e-mail adress is for example " +
                            "john@yahoo.com")
                ])

    days = SelectField('Interval of validity',
                choices=[
                    ("30", "1 month"),
                    ("90", "3 months"),
                    ("362", "1 year")
                ])

    garant_mail = TextField("Guarantee's e-mail", [
                validators.Regexp(
                    '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$',
                    message="Guarantee's e-mail must be in domain FZU.CZ.")
                ])


class Enroll_cz(Form):
    language = SelectField('Jazyk',
                choices=[
                    ("cs", "CZ Česky"),
                    ("en", "EN English")
                ],
                default="cz")

    first_name = TextField('Jméno', [
                validators.Required(
                    message=u"Jméno musí být vyplněno.")
                ])

    last_name = TextField('Příjmení', [
                validators.Required(
                    message=u"Příjmení musí být vyplněno.")
                ])

    phone = TextField('Telefon', [
                validators.regexp(
                    '^(\+420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$',
                    message=u"Povolený formát je:<ul>" +
                            "<li> +420 123 123 123</li>" +
                            "<li> 123 123 123</li>" +
                            "<li>123123123</li>" +
                            "</ul>")
                ])

    mail = TextField('E-mail', [
                validators.Regexp(
                    '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$',
                    message=u"Správný formát e-mailu " +
                            "je například karel@fzu.cz")
                ])

    days = SelectField('Doba platnosti',
                choices=[
                    ("30", "1 měsíc"),
                    ("90", "3 měsíce"),
                    ("362", "1 rok")
                ])

    garant_mail = TextField("E-mail ručitele", [
                validators.Regexp(
                    '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$',
                    message=u"Ručitelův e-mail musí být v doméně fzu.cz.")
                ])


class Login(Form):
    username = TextField('Username', [
                validators.Required(
                    message="Please input your email login " +
                    "(without @fzu.cz.)")
                ])

    password = PasswordField('Password', [
                validators.Required(
                    message="Please input your email password.")
                ])
