# -*- coding: utf-8 -*-

from socket import *

import subprocess
import string

#Estabelecendo a porta
serverPort = 9003
#Criando socket TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#Associando a porta 9003 com o socket do servidor
serverSocket.bind(("",serverPort))
#Espera pelos pacotes do cliente
serverSocket.listen(1)

bar = "|"
pv = ";"
maior = ">"
menor = "<"
ps = "1 "
df = "2 "
finger = "3 "
uptime = "4 "


while True:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	sentence = sentence.replace("REQUEST ","")
	if bar in sentence:
		sentence = sentence.replace(bar, "")
	if pv in sentence:
		sentence = sentence.replace(pv, "")
	if maior in sentece:
		sentence = sentence.replace(maior, "")
	if menor in sentece:
		sentence = sentence.replace(menor, "")
	if ps in sentence:
		sentence = sentence.replace(ps,"ps")
		numero = ps
	if df in sentence:
		sentence = sentence.replace(df,"df")
		numero = df
	if finger in sentence:
		sentence = sentence.replace(finger,"finger")
		numero = finger
	if uptime in sentence:
		sentence = sentence.replace(uptime,"uptime")
		numero = uptime

	# executa num subcomando
	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE " + numero + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()
