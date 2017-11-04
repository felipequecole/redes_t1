# -*- coding: utf-8 -*- 

from socket import *

def sendMsg(comando):
	serverName = gethostname()
	serverPort = 9003  # ainda nao define a porta por parametro, fixei na 9003 para testes

	clientSocket = socket(AF_INET,SOCK_STREAM)
	
	try: 
    		clientSocket.connect((serverName, serverPort))
    		if comando:
      			clientSocket.send(comando)
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
    
