# -*- coding: utf-8 -*-

from socket import *
import struct


def carry_add(a,b):
	c = a + b
	return ((c & 0xffff) + (c >> 16))


def checksum(dados, op):
	s = 0
	for i in range(0, len(dados), 2):
		w = ord(dados[i]) + (ord(dados[i+1]) << 8)
		s = carry_add(s, w)
	if(op):
		return s & 0xffff
	else:
		return ~s & 0xffff



def create_header(comando):
	comando = comando.split(' ')
	protocol_version = 2
	ihl = 16
	type_of_service = 0
	total_length = 99
	identification = 1
	ttl = 10
	protocol = int(comando[0])
	source = inet_aton(gethostbyname(gethostname()))
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
	headerChecksum = ''
	for o in options:
		 headerChecksum = header + struct.pack('!c', o)
	checksum = checksum(headerChecksum, 0)
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
	if (len(comando) > 0):
		header = create_header(comando)
		if (len(header) > 0):
			try:
				clientSocket.connect((serverName, serverPort))
				clientSocket.send(header)
				comando = ""
				dados = clientSocket.recv(10240)
				dados = testar_dados(dados)
				clientSocket.close()

			except Exception:
				dados = "Socket sem conexao!"
		else:
			dados = "Erro ao criar cabeçalho!"
	else:
		dados = "Comando inválido!"

	return dados

def testar_dados (rcv): 	# posteriormente talvez seja aqui que a gente defina os roles do cabeçalho
	lista = rcv.split()
	if lista[0] != "RESPONSE":
        	return "Resposta enviada eh incoerente!"

	lista = rcv.split("RESPONSE")

	return  lista[1]
