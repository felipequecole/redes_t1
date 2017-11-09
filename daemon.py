# -*- coding: utf-8 -*-

from socket import *
import subprocess
import string
import sys, io, struct
import thread

# class Daemon(threading.Thread):
# 	def run(self, socket):
#

def parse_header(message):
	header = io.BytesIO(message)
	protocol_version = str(struct.unpack('!h',header.read(2))[0])
	ihl = str(struct.unpack('!h',header.read(2))[0])
	type_of_service = str(struct.unpack('!i', header.read(4))[0])
	total_length = str(struct.unpack('!Q', header.read(8))[0])
	identification = str(struct.unpack('!Q', header.read(8))[0])
	flags = []
	for i in range(3):
		flags.append(str(struct.unpack('!c', header.read(1))[0]))
	offset = []
	for j in range(5):
		offset.append(str(struct.unpack('!c', header.read(1))[0]))
	ttl = str(struct.unpack('!i', header.read(4))[0])
	sentence = str(struct.unpack('!i', header.read(4))[0])
	sentence += '  '
	checksum = str(struct.unpack('!Q', header.read(8))[0])
	op = header.read()
	cmd = ''
	for i in op:
		cmd += str(struct.unpack('!c', i)[0])
	sentence += cmd
	return sentence

def send_packet(socket):
	packet = socket.recv(1024)
	sentence = parse_header(packet) + ' '
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
	if df in sentence:
		sentence = sentence.replace(df,"df")
	if finger in sentence:
		sentence = sentence.replace(finger,"finger")
	if uptime in sentence:
		sentence = sentence.replace(uptime,"uptime")

	# executa num subcomando
	comando = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = comando.communicate()
	resposta = "RESPONSE " + resposta
	connectionSocket.send(resposta)
	connectionSocket.close()



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
	try:
		thread.start_new_thread(send_packet, (connectionSocket,))
	except Exception as e:
		raise
