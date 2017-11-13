# -*- coding: utf-8 -*-

from socket import *
import struct
from io import BytesIO

sequence = 0 # variavel global para identificar o pacote


def calc_checksum(dados, op):
	somaTotal = 0 #inicializa a soma total dos dados com 0
	for i in range(0, len(dados)): #percorre a string de byte passada como parametro de 2 em 2 bytes (16 em 16 bits)
		somaTotal += ord(dados[i])
	if(op):
		return somaTotal & 0xffff #retorna o valor da soma total sem invertir os bits
	else:
		return ~somaTotal & 0xffff #retorna o valor da soma total invertendo todos os bits



def create_header(comando):
	# declarar tudo que usaremos para fazer o cabeçalho
	header = BytesIO()
	comando = comando.split(' ')
	options = ''
	for i in range(len(comando)): # loop para ler e identificar cada argumento do comando
		if(i != 0 and i != len(comando)-1):
			options += comando[i] + ' '
		if(i == len(comando)-1):
			options += comando[i]
	protocol_version = 2
	ihl = 6 if (len(options) > 0) else 5	# caso haja options, o cabeçalho contem 1 linha a mais (de 32 bits)
	type_of_service = 0
	global sequence
	sequence += 1 # pega o próximo da sequencia
	ttl = 10	# valor arbitrário
	protocol = int(comando[0])
	source = inet_aton(gethostbyname(gethostname()))
	destination = inet_aton(gethostbyname(gethostname())) # TODO: verificar como pegar esse IP
	total_length = (ihl * 4) + len(options)
	aux = ((protocol_version << 4) & 0xf0) | ihl # coloca em aux os valores de versão do protocolo e ihl
	aux = (aux << 8) & 0xff00 | type_of_service	# concatena com tipo de serviço
	primeira_linha = struct.pack('!HH', aux, total_length)	# escreve a primeira linha do cabeçalho em bytes
	segunda_linha = struct.pack('!HH', sequence, 0) 	# 0 porque é requisição + offset
	aux = ((ttl << 8) & 0xff00) | protocol	# concatena ttl e protocolo
	op_bin = ''
	for char in options:
		op_bin += struct.pack('!c', char)	# converte as opções para bytes
	aux_check = primeira_linha + segunda_linha + struct.pack('!H', aux) + source + destination + op_bin
	terceira_linha = struct.pack('!HH', aux, calc_checksum(aux_check, 0))
	header.write(primeira_linha)	# monta todo o cabeçalho
	header.write(segunda_linha)
	header.write(terceira_linha)
	header.write(source)
	header.write(destination)
	header.write(op_bin)
	header.seek(0)	# volta o ponteiro de leitura pra posiçao original
	return header.read()	# retorna todo o conteúdo


# Responsável por fazer o parse de mensagem recebida
def parse_header(message):
	header = BytesIO(message)
	aux = struct.unpack('!H', header.read(2))[0]
	protocol_version = (aux >> 8) >> 4	# faz o parse da versão do protocolo
	ihl = (aux >> 8) & 0x0f	# e do ihl
 	type_of_service = aux & 0x00ff
 	total_length = struct.unpack('!H', header.read(2))[0]
	identification = struct.unpack('!H', header.read(2))[0]
	aux = struct.unpack('!H', header.read(2))[0]
	flags = []
	flags.append(aux & 0x80 >> 7)
	flags.append(aux & 0x40 >> 6)
	flags.append(aux & 0x20 >> 5)
	aux = struct.unpack('!h', header.read(2))[0]
	ttl = aux >> 8
	protocol = aux & 0x00ff
	checksum = struct.unpack('!H', header.read(2))[0]
	headerChecksum = BytesIO(message)
	check = headerChecksum.read(10)
	headerChecksum.read(2)
	check = check + headerChecksum.read(8)
	check = calc_checksum(check,1)+checksum
	source = inet_ntoa(header.read(4))
	destination = inet_ntoa(header.read(4))
	header.read(4) # pular a parte de options (deve estar vazia)
	aux = header.read(1)
	data = ''
	while(aux != ''):
		data += aux
		aux = header.read(1)
	if(check != 0xffff):
		data = 'Erro na verificação do checksum: ' + str(checksum)
	return {'cmd': str(protocol),
			'ttl' : ttl,
			'identification' : identification,
			'flags': flags,
			'protocol': protocol,
			'source': source,
			'destination': destination,
			'data': data,
			'raw' : message
			}

def sendMsg(comando, maquina):
	serverName = gethostname()	# como tudo está rodando na mesma VM, pega o endereço local
	serverPort = 9000 + maquina  # cada porta seria uma "máquina", então é aqui que é feita a seleção
	dados = {}
	clientSocket = socket(AF_INET,SOCK_STREAM)	# cria o socket
	if (len(comando) > 0):
		header = create_header(comando) # cria o header para requisição
		if (len(header) > 0):	#  se o header foi criado com sucesso, envia para o socket
			try:
				clientSocket.connect((serverName, serverPort))
				clientSocket.send(header)
				comando = ""
				response = clientSocket.recv(10240)
				clientSocket.close()
				dados = parse_header(response)

			except Exception:
				raise
				dados['data'] = "Socket sem conexao!"
		else:
			dados['data'] = "Erro ao criar cabeçalho!"
	else:
		dados['data'] = "Comando inválido!"

	return dados
