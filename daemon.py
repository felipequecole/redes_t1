# -*- coding: utf-8 -*- 

from socket import *

import subprocess
import string
import sys, io, struct


def parse_header(message):
	header = io.BytesIO(message)
	header.read(36) # so jogando fora parte do header rs
	return str(struct.unpack('!i', header.read(4))[0])



serverPort = 9001
try:
	if(sys.argv[1] == '--port'):
		serverPort = int(sys.argv[2])
except Exception:
	serverPort += 1

#Criando socket TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#Associando a porta 9003 com o socket do servidor
serverSocket.bind(("",serverPort))
#Espera pelos pacotes do cliente
serverSocket.listen(1)

ps = "1 "
df = "2 "
finger = "3 "
uptime = "4 "
bar = "|"
pv = ";"
maior = ">"
menor = "<"


while True:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	sentence = parse_header(sentence) + ' '
	numero = 0
	if bar in sentence:
		sentence = sentence.replace(bar, "")
	if pv in sentence:
		sentence = sentence.replace(pv, "")
	if maior in sentence:
		sentence = sentence.replace(maior, "")
	if menor in sentence:
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

