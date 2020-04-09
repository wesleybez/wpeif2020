import time
import threading
import stomp
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')
HOST = config.get('geral','host')
PORT = config.get('geral','port')

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_stomp_publish_non_autenticated.csv","w") 

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        print('received a message "%s"' % message)


def worker(cont):
    t_inicio = time.process_time()
    #stomp client
    #docker run -p 61616:61616 -p 8161:8161 rmohr/activemq
    #conn = stomp.StompConnection12([(HOST, PORT)],auto_content_length=True)
    conn = stomp.Connection([(HOST, PORT)]) #activemq rodando stomp
    
    #conn = stomp.Connection()
    conn.set_listener('', MyListener())
    conn.start()
    #conn.connect('sensor1', 'senha1', wait=True)
    conn.connect()
    
    #
    t_connection = time.process_time()
    td_connection = t_connection - t_inicio 
    #publicando
    conn.send(body="aleatorio_"+str(cont), destination='/casa/teste')
    t_publish = time.process_time() 
    td_publish = t_publish - t_connection
    #
    #time.sleep(1000)
    #inscricao
    #conn.subscribe(destination='/queue/test', id=1, ack='auto')

    #time.sleep(1000)
    t_subscribe = time.process_time()
    td_subscribe = t_subscribe - t_publish
    
    conn.disconnect()
    t_disconnect = time.process_time()
    td_disconnect = t_disconnect - t_subscribe
    
    medicoes.write(" "+str(cont+1)
                   +","+str(t_inicio*FATOR_MULT)
                   +","+str(td_connection*FATOR_MULT)
                   +","+str(td_publish*FATOR_MULT)
                   +","+str(td_subscribe*FATOR_MULT)
                   +","+str(td_disconnect*FATOR_MULT)
                   +"\n")
    #print (" ",cont+1,",",t_inicio*1000,",",td_connection*1000,",",td_publish*1000,",",td_subscribe*1000,",",td_disconnect*1000)

medicoes.write("thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000] \n")
#print ("thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000]")    
clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)
medicoes.close()