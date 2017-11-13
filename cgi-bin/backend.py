# -*- coding: utf-8 -*-

from socket import *
import struct
from io import BytesIO

# def carry_add(a,b):
# 	c = a + b
# 	return ((a + b & 0xffff) + (a + b >> 16))

sequence = 0 # variavel global para identificar o pacote


def calc_checksum(dados, op):
	somaTotal = 0 #inicializa a soma total dos dados com 0
	#  antes tava com passo 2
	for i in range(0, len(dados)): #percorre a string de byte passada como parametro de 2 em 2 bytes (16 em 16 bits)
		# palavra = ord(dados[i]) + (ord(dados[i+1]) << 8) #concatena 2 bytes formando uma palavra de 16 bits
		# somaTotal = ((somaTotal + palavra & 0xffff) + (somaTotal + palavra >> 16)) #soma ao total a soma total a próxima palavra
		somaTotal += ord(dados[i])
		# s = carry_add(s, w)
	if(op):
		return somaTotal & 0xffff #retorna o valor da soma total sem invertir os bits
	else:
		return ~somaTotal & 0xffff #retorna o valor da soma total invertendo todos os bits



def create_header(comando):
	# declarar tudo que usaremos para fazer o cabeçalho
	header = BytesIO()
	comando = comando.split(' ')
	options = ''
	for i in range(len(comando)):
		if(i != 0 and i != len(comando)-1):
			options += comando[i] + ' '
		if(i == len(comando)-1):
			options += comando[i]
	protocol_version = 2
	ihl = 6 if (len(options) > 0) else 5
	type_of_service = 0
	total_length = 0 # calcular
	global sequence
	sequence += 1
	ttl = 10	# valor arbitrário
	protocol = int(comando[0])
	source = inet_aton(gethostbyname(gethostname()))
	destination = inet_aton(gethostbyname(gethostname())) # TODO: verificar como pegar esse IP

	# header = struct.pack('!hhiQ', protocol_version, ihl, type_of_service, total_length)
	# header += struct.pack('!Qccc', identification, '1', '1', '1')

	# começa a escrever o cabeçalho
	aux = ((protocol_version << 4) & 0xf0) | ihl
	aux = (aux << 8) & 0xff00 | type_of_service
	primeira_linha = struct.pack('!HH', aux, ihl*4)
	segunda_linha = struct.pack('!HH', sequence, 0) 	# 0 porque é requisição + offset
	aux = ((ttl << 8) & 0xff00) | protocol
	op_bin = ''
	for char in options:
		op_bin += struct.pack('!c', char)
	aux_check = primeira_linha + segunda_linha + struct.pack('!H', aux) + source + destination + op_bin
	terceira_linha = struct.pack('!HH', aux, calc_checksum(aux_check, 0))
	header.write(primeira_linha)
	header.write(segunda_linha)
	header.write(terceira_linha)
	header.write(source)
	header.write(destination)
	header.write(op_bin)
	header.seek(0)
	return header.read()

	# for p in range (5):
	# 	header += struct.pack('!c', '0')
	# headerChecksum = header
	# for o in options:
	# 	headerChecksum += struct.pack('!c', o)
	# checksum = calc_checksum(headerChecksum+source+destination, 0)
	# header += struct.pack('!iiQ', ttl, protocol, checksum)
	# header += source
	# header += destination
	# # # TODO adicionar os address no header
	# for o in options:
	# 	header += struct.pack('!c', o)
	# return header
	# por enquanto vai ignorar a parte de source e dest address

def parse_header(message):
	header = BytesIO(message)
	aux = struct.unpack('!H', header.read(2))[0]
	protocol_version = (aux >> 8) >> 4
	ihl = (aux >> 8) & 0x0f
	ihl = aux & 0x00ff
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
	check = check + headerChecksum.read()
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
		data = 'Erro na verificação do checksum: ' + str(check)
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
	serverName = gethostname()
	serverPort = 9000 + maquina  # ainda nao define a porta por parametro, fixei na 9003 para testes
	dados = {}
	clientSocket = socket(AF_INET,SOCK_STREAM)
	if (len(comando) > 0):
		header = create_header(comando)
		if (len(header) > 0):
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
