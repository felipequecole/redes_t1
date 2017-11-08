# -*- coding: utf-8 -*-

from socket import *
import struct


def checksum(dados):
	


def create_header(comando):
	comando = comando.split(' ')
	protocol_version = 2
	ihl = 16
	type_of_service = 0
	total_length = 99
	identification = 1
	ttl = 10
	protocol = int(comando[0])
	checksum = 282	# TODO: checksum
	source = socket.gethostbyname(socket.gethostname())
	destination = '192.168.56.101' # TODO: verificar como pegar esse IP
	options = ''
	for i in range(len(comando)):
		if(i != 0 and i != len(comando)-1):
			options += comando[i] + ' '
		if(i == len(comando)-1):
			options += comando[i]
	header = struct.pack('!hhiQ', protocol_version, ihl, type_of_service, total_length)
	header += struct.pack('!Qccc', identification, '1', '1', '1')
	for p in range (5):
		header += struct.pack('!c', '0')
	header += struct.pack('!iiQ', ttl, protocol, checksum)
	# TODO adicionar os address no header
	for o in options:
		header += struct.pack('!c', o)
	return header
	# por enquanto vai ignorar a parte de source e dest address

def parse_message(message):
	pass

def sendMsg(comando, maquina):
	serverName = gethostname()
	serverPort = 9000 + maquina  # ainda nao define a porta por parametro, fixei na 9003 para testes

	clientSocket = socket(AF_INET,SOCK_STREAM)

	try:
    		clientSocket.connect((serverName, serverPort))
    		if comando:
      			clientSocket.send(create_header(comando))
			comando = ""
			dados = clientSocket.recv(1024)
			dados = testar_dados(dados)
		else:
			dados = "Impossivel gerar comando!"

		clientSocket.close()

	except Exception:
		dados = "Socket sem conexao!"

	return dados

def testar_dados (rcv): 	# posteriormente talvez seja aqui que a gente defina os roles do cabeçalho
	lista = rcv.split()
	if lista[0] != "RESPONSE":
        	return "Resposta enviada eh incoerente!"

	lista = rcv.split("RESPONSE")

	return  lista[1]
