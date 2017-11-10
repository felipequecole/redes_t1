# -*- coding: utf-8 -*-

from socket import *
import struct

# def carry_add(a,b):
# 	c = a + b
# 	return ((a + b & 0xffff) + (a + b >> 16))


def calc_checksum(dados, op):
	somaTotal = 0 #inicializa a soma total dos dados com 0
	for i in range(0, len(dados), 2): #percorre a string de byte passada como parametro de 2 em 2 bytes (16 em 16 bits)
		palavra = ord(dados[i]) + (ord(dados[i+1]) << 8) #concatena 2 bytes formando uma palavra de 16 bits
		somaTotal = ((somaTotal + palavra & 0xffff) + (somaTotal + palavra >> 16)) #soma ao total a soma total a próxima palavra
		# s = carry_add(s, w)
	if(op):
		return somaTotal & 0xffff #retorna o valor da soma total sem invertir os bits
	else:
		return ~somaTotal & 0xffff #retorna o valor da soma total invertendo todos os bits



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
	destination = inet_aton('192.168.56.101') # TODO: verificar como pegar esse IP
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
	headerChecksum = header
	for o in options:
		headerChecksum += struct.pack('!c', o)
	checksum = calc_checksum(headerChecksum+source+destination, 0)
	header += struct.pack('!iiQ', ttl, protocol, checksum)
	header += source
	header += destination
	# # TODO adicionar os address no header
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
