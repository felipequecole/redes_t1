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
	isInDiv = False
	gambiarraPS = False
	for comando in comandos:
		if ('maq' + str(i) + '_' + comando) in form:
			if (isInDiv == False):
				print('<div class="col-sm-12" id="col-' + str(i)+ '">')
				isInDiv = True
			# print("<p>")
			try:
				if(form.getvalue('maq' + str(i) + '-' + comando)):
					message = backend.sendMsg(comandos[comando] +' '+' '+ form.getvalue('maq' + str(i) + '-' + comando), i)
				else:
					message = backend.sendMsg(comandos[comando], i)
					if (comando == 'ps'):
						gambiarraPS = True
			except Exception as e:
				message = {'data': 'Erro ao processar requisição. Verifique se o daemon está rodando.',
							'cmd' : 'error'}

			split = message['data'].split('\n')


			header = True
			print('<h3> <b>Comando: </b>' + comando + ' - <b> Máquina: </b> ' + str(i) + '</h3>')
			try:
				for ms in split:
					if (header and comando != 'uptime' and message['cmd'] != 'error'):
						header = False
						print ('<table class="table">')
						print('<thead class="thead-dark">')
						print('<tr>')
						for part in ms.split(' '):
							if (part != ''):
								if (gambiarraPS):
									gambiarraPS = False
									continue
								print('<th scope="col">' + part + '</th>')
						print('</tr>')
						print('</thead>')
						print('<tbody>')
					elif (comando != 'uptime' and message['cmd'] != 'error'):
						print('<tr>')
						for part in ms.split(' '):
							if (part != ''):
								print('<td>' + part + '</td>')
						print('<tr>')
					else:
						print('<p>')
						print(ms)
						print('</p>')
				if (comando != 'uptime' and message['cmd'] != 'error'):
					print('</tbody></table>')
				print('<p></p>')
			except Exception as e:
				print('<p>' + e + '</p>')
	if (isInDiv):
		print('</div>')
		isInDiv = False


print('<div class="col-sm-12">')
print('<p><a href=\"/\"> <button type=\"button\" class=\"btn btn-primary\">Voltar</button> </a></p>')
print('</div>')
print('</body>')
