#!/usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print('<link href=\"/css/bootstrap.min.css\" rel=\"stylesheet\">')
print("Hello World!")

comandos = ['ps', 'df', 'finger', 'uptime']

for i in range (1,4):
	for comando in comandos: 
		if ('maq' + str(i) + '_' + comando) in form:
			print("<p>")
			print("Maq" + str(i) + " pediu " + comando.upper())
			try:
				print(form.getlist("maq1-" + comando)[0])
			except IndexError:
		 		print("Nao tem numero")

print('<p><a href=\"/\"> <button type=\"button\" class=\"btn btn-primary\">Voltar</button> </a></p>')