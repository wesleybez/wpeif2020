#https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019
import pika
import time
import threading
import ConfigParser
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


config = ConfigParser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')
HOST = config.get('geral','host')
PORT = config.get('geral','port')

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_amqp_publish_non_auth.csv","w") 

def callback(ch, method, properties, body):
   i = 1# print(" [x] Received %r" % body)

def worker(cont):
    t_inicio = time.clock()
    #mqtt client
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
            port=PORT)
        )
    channel = connection.channel()
    channel.queue_declare(queue='casa/teste')   
    #client = mqtt.Client(protocol=mqtt.MQTTv31)
    t_connection = time.clock()
    td_connection = t_connection - t_inicio 
    #publicando
    channel.basic_publish(exchange='',
                      routing_key='casa/teste',
                      body="aleatorio_"+str(cont))
    t_publish = time.clock() 
    td_publish = t_publish - t_connection
    #
    #time.sleep(1000)
    #client.subscribe("casa/teste_2")
    #channel.basic_consume('casa/teste',callback,True)
    #channel.start_consuming()
#    print response.pretty_print()
    #time.sleep(1000)
    t_subscribe = time.clock() 
    td_subscribe = t_subscribe - t_publish
    
    connection.close()
    t_disconnect = time.clock()
    td_disconnect = t_disconnect - t_subscribe
    
    medicoes.write(" "+str(cont+1)
                   +","+str(t_inicio*FATOR_MULT)
                   +","+str(td_connection*FATOR_MULT)
                   +","+str(td_publish*FATOR_MULT)
                   +","+str(td_subscribe*FATOR_MULT)
                   +","+str(td_disconnect*FATOR_MULT)
                   +"\n")    

clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)