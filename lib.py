# -*- coding: utf-8 -*-

import yaml, subprocess, pymysql, smtplib
from jinja2 import Template
from email.mime.text import MIMEText

def load_yaml(file_path):
	try:
		with open(file_path, 'r') as F:
			return yaml.load(F)
	except ImportError:
		print("import yaml is required")
		exit(1)




def send_mail(smtp, template, data):
	# poskladani zpravy z predlohy
	with open(template, 'r', encoding="utf-8") as TPL:
		tpl = Template(TPL.read())
		
	msg = MIMEText(tpl.render(**data), 'plain', _charset='utf-8')
	#msg = tpl.render(**data)
	msg['MIME-Version:'] = "1.0"
	msg['To'] = data['garant_mail']
	msg['From'] = smtp['sender']
	msg['Subject'] = 'FZU-GUEST {first_name} {last_name}'.format_map(data)
	msg["Content-Type"] = "text/plain;charset=UTF-8;format=flowed"
	msg["Content-Transfer-Encoding"] = '8bit'
	msg['X-Sender'] = smtp['sender']
	print(msg.as_string())
	
	try:
		server = smtplib.SMTP(smtp['server'])
		server.starttls()
		server.login(smtp['login'], smtp['password'])
		server.sendmail(smtp['sender'], data['garant_mail'], msg.as_string())
		return True
	
	except IOError as err:
		print("Server unavaliable: ", err)
		return False



def db_exec(db, query = None, debug=False):
	con = False
	try:
		con = pymysql.connect(host=db['server'], user=db['login'], passwd=db['password'], db=db['db'])
		cursor = con.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		ret =  [line for line in cursor]
		if debug: print('Err')   #ret)
		return ret
	except pymysql.Error as err:
		print(err)
		return False
	finally:
		if con:
			cursor.close()
			con.close()

def get_mac(ipaddress):
	print(ipaddress)
	try: 
		print("hledam MAC")
		out = subprocess.check_output(["/home/enroll/enroll/get_arp.sh", 
										ipaddress]).decode('utf-8')
		print(out)
		return out
	except IOError as err:
		print(err)
		return False

def str2mac(mac):
	i = 1 
	ret = ""
	for ch in mac:
		ret += ch
		if i == 2:
			ret += ":"
			i = 0
		i += 1
	return ret[:-1]


def valid_grant(smtp, username, password):
	try:
		server = smtplib.SMTP(smtp['server'])
		if server.login(username, password):
			return True
		else:
			return False
	except TimeoutError:
		return False
