#!/usr/bin/env python
import cgitb
import cgi
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("Hello World!")
if "maq1_ps" in form:
	print("<p>")
	print("Maq1 pediu PS")
	print(form.getlist("maq1-ps")[0])
	print("</p>")
if "maq2_ps" in form:
	print("<br>")
	print("Maq2 pediu PS")
	print(form.getlist("maq2-ps")[0])
if "maq3_ps" in form:
	print("<br>")
	print("Maq3  pediu PS")
	print(form.getlist("maq3-ps")[0])
