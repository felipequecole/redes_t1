# -*- coding: utf-8 -*-

from socket import *
import subprocess
import string
import sys, io, struct
import thread

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


def create_header(message, protocol, source, destination, ttl, identification):
	# declarar tudo que usaremos para fazer o cabeçalho
	header = io.BytesIO()
	protocol_version = 2
	ihl = 5 	# tem o campo Data
	type_of_service = 0
	total_length = 0 # calcular
	ttl = ttl - 1
	# header = struct.pack('!hhiQ', protocol_version, ihl, type_of_service, total_length)
	# header += struct.pack('!Qccc', identification, '1', '1', '1')

	# começa a escrever o cabeçalho
	aux = ((protocol_version << 4) & 0xf0) | ihl
	aux = (aux << 8) & 0xff00 | type_of_service
	primeira_linha = struct.pack('!HH', aux, ihl*4)
	segunda_linha = struct.pack('!HH', identification, 0xe0) 	# 0xE0 response + offset
	aux = ((ttl << 8) & 0xff00) | protocol
	op_bin = struct.pack('!Q', 0)
	aux_check = primeira_linha + segunda_linha + struct.pack('!H', aux) + source + destination
	terceira_linha = struct.pack('!hH', aux, calc_checksum(aux_check, 0))
	header.write(primeira_linha)
	header.write(segunda_linha)
	header.write(terceira_linha)
	header.write(inet_aton(source))
	header.write(inet_aton(destination))
	header.write(op_bin)
	header.write(message)
	header.seek(0)
	return header.read()


def parse_header(message):
	header = io.BytesIO(message)
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
	aux = struct.unpack('!H', header.read(2))[0]
	ttl = aux >> 8
	protocol = aux & 0x00ff
	checksum = struct.unpack('!H', header.read(2))[0]
	headerChecksum = io.BytesIO(message)
	check = headerChecksum.read(10)
	headerChecksum.read(2)
	check = check + headerChecksum.read()
	check = hex(calc_checksum(check,1)+checksum))
	source = inet_ntoa(header.read(4))
	destination = inet_ntoa(header.read(4))
	aux = header.read(1)
	args = ''
	while(aux != ''):
		args += aux
		aux = header.read(1)
	return {'cmd': str(protocol) + ' ' + args,
			'ttl' : ttl,
			'identification' : identification,
			'flags': flags,
			'protocol': protocol,
			'source': source,
			'destination': destination
			}

	# ihl = str(struct.unpack('!h',header.read(2))[0])
	# type_of_service = str(struct.unpack('!i', header.read(4))[0])
	# total_length = str(struct.unpack('!Q', header.read(8))[0])
	# identification = str(struct.unpack('!Q', header.read(8))[0])
	# flags = []
	# for i in range(3):
	# 	flags.append(str(struct.unpack('!c', header.read(1))[0]))
	# offset = []
	# for j in range(5):
	# 	offset.append(str(struct.unpack('!c', header.read(1))[0]))
	# ttl = str(struct.unpack('!i', header.read(4))[0])
	# sentence = str(struct.unpack('!i', header.read(4))[0])
	# sentence += '  '
	# print sentence
	# checksum = str(struct.unpack('!Q', header.read(8))[0])
	# soucer = inet_ntoa(header.read(4))
	# dest = inet_ntoa(header.read(4))
	# print dest
	# op = header.read()
	# cmd = ''
	# for i in op:
	# 	cmd += str(struct.unpack('!c', i)[0])
	# 	print cmd
	# sentence += cmd
	# return sentence

def send_packet(socket):
	packet = socket.recv(1024)
	mensagem = parse_header(packet)
	comando = mensagem['cmd'] # TODO colocar espaco no parse
	if bar in comando:
		comando = comando.replace(bar, "")
	if pv in comando:
		comando = comando.replace(pv, "")
	if maior in comando:
		comando = comando.replace(maior, "")
	if menor in comando:
		comando = comando.replace(menor, "")
	if ps in comando:
		comando = comando.replace(ps,"ps")
	if df in comando:
		comando = comando.replace(df,"df")
	if finger in comando:
		comando = comando.replace(finger,"finger")
	if uptime in comando:
		comando = comando.replace(uptime,"uptime")

	# executa num subcomando
	subprocesso = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
	(resposta, err) = subprocesso.communicate()
	if (mensagem['ttl'] > 0):
		resposta = create_header(resposta, mensagem['protocol'], mensagem['destination'],
								mensagem['source'], mensagem['ttl'], mensagem['identification'])
	else:
		resposta = create_header('Seu pacote foi rejeitado (TTL = 0)', mensagem['protocol'], mensagem['destination'],
								mensagem['source'], mensagem['ttl'], mensagem['identification'])
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
