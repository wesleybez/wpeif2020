#http://alissonmachado.com.br/python-threads/
#https://realpython.com/intro-to-python-threading/
import threading
import resource

import paho.mqtt.client as mqtt
import time
import logging
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_mqtt_publish_auth.csv","w")
memoria  = open("/home/wesley/"+time.strftime('%Y%m%d')+"_memory_mqtt_publish_auth.csv","w")




#def on_connect(client, userdata, flags, rc):
    #if rc==0:
    #    print("connected OK Returned code=",rc)
    #else:
    #    print("Bad connection Returned code=",rc)
    
    
def worker(cont):
    t_inicio = time.clock()
    m_inicio = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #mqtt client
    client = mqtt.Client("note"+str(cont),True, None,protocol=mqtt.MQTTv31)    
    client.enable_logger(logger)
    #client = mqtt.Client(protocol=mqtt.MQTTv31)
    #client.on_connect = on_connect
    client.username_pw_set("sensor"+str((cont%10)+1), "senha"+str((cont%10)+1))
    client.connect("172.17.0.1", 1883)
    t_connection = time.clock()
    m_connection = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    td_connection = t_connection - t_inicio
    md_connection = m_connection - m_inicio 
    
    client.publish("casa/teste", "aleatorio_"+str(cont))
    
    t_publish = time.clock() 
    m_publish = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    td_publish = t_publish - t_connection
    md_publish = m_publish - m_connection
    #
    #time.sleep(1000)
    #client.subscribe("casa/teste_2")
    #time.sleep(1000)
    t_subscribe = time.clock() 
    m_subscribe = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    td_subscribe = t_subscribe - t_publish
    md_subscribe = m_subscribe - m_publish
    #loop para visualizacao dos callbacks
    client.loop_start()
    
    client.disconnect()
    
    t_disconnect = time.clock()
    m_disconnect = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    td_disconnect = t_disconnect - t_subscribe
    md_disconnect = m_disconnect - m_subscribe
    
    medicoes.write(" "+str(cont+1)
                   +","+str(t_inicio*FATOR_MULT)
                   +","+str(td_connection*FATOR_MULT)
                   +","+str(td_publish*FATOR_MULT)
                   +","+str(td_subscribe*FATOR_MULT)
                   +","+str(td_disconnect*FATOR_MULT)
                   +"\n")
    
    memoria.write(" "+str(cont+1)
                   +","+str(m_inicio)
                   +","+str(md_connection)
                   +","+str(md_publish)
                   +","+str(md_subscribe)
                   +","+str(md_disconnect)
                   +"\n")
    #print " ",cont+1,",",t_inicio*FATOR_MULT,",",td_connection*FATOR_MULT,",",td_publish*FATOR_MULT,",",td_subscribe*FATOR_MULT,",",td_disconnect*FATOR_MULT
    
#cabecalho csv
#medicoes.write("thread ,inicio ,conexao ,publicacao ,inscricao ,fim \n")
#print "thread ,inicio ,conexao ,publicacao ,inscricao ,fim"

clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)
#client.subscribe("casa/teste_2")