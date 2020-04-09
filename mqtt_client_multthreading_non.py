#http://alissonmachado.com.br/python-threads/
#https://realpython.com/intro-to-python-threading/
import threading
import resource

import paho.mqtt.client as mqtt
import time
import logging
import ConfigParser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


config = ConfigParser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_mqtt_publish_non_auth.csv","w")
memoria  = open("/home/wesley/"+time.strftime('%Y%m%d')+"_memory_mqtt_publish_non_auth.csv","w")

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    
    
def worker(cont):
    t_inicio = time.clock()
    m_inicio = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #mqtt client
    client = mqtt.Client("note"+str(cont),True, None,protocol=mqtt.MQTTv31)   
    client.enable_logger(logger) 
    #client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
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
    #client.loop_forever()
    
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
    #print " ",cont+1,",",t_inicio*1000,",",td_connection*1000,",",td_publish*1000,",",td_subscribe*1000,",",td_disconnect*1000
    memoria.write(" "+str(cont+1)
                   +","+str(m_inicio)
                   +","+str(md_connection)
                   +","+str(md_publish)
                   +","+str(md_subscribe)
                   +","+str(md_disconnect)
                   +"\n")
#cabecalho csv
medicoes.write("thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000] \n")
#print "thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000]"

clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)
medicoes.close()
#client.subscribe("casa/teste_2")