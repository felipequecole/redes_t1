#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import cgi
import backend
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print('<html>')
print('<head>')
print('<meta charset=\"utf-8\">')
print('<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')
print('<link href=\"/css/bootstrap.min.css\" rel=\"stylesheet\">')
print('<title>Trabalho Redes</title>')
print('</head>')
print('<body>')

comandos = {
		'ps' : '1 ',
		'df' : '2 ',
		'finger': '3 ',
		'uptime': '4 '
	}

for i in range (1,4):
	for comando in comandos:
		if ('maq' + str(i) + '_' + comando) in form:
			print("<p>")
			if(form.getvalue('maq' + str(i) + '-' + comando)):
				message = backend.sendMsg(comandos[comando] +' '+' '+ form.getvalue('maq' + str(i) + '-' + comando), i)
			else:
				message = backend.sendMsg(comandos[comando], i)
			split = message.split('\n')
			for ms in split:
				print(ms)
				print('</p><p>')
			print('</p>')
			# print("Maq" + str(i) + " pediu " + comando.upper())
			# try:
			# 	print(form.getlist("maq1-" + comando)[0])
			# except IndexError:
		 # 		print("Nao tem numero")

print('<p><a href=\"/\"> <button type=\"button\" class=\"btn btn-primary\">Voltar</button> </a></p>')
print('</body>')
