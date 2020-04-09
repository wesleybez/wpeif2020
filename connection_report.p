set grid

set terminal pngcairo size 700,524 enhanced font 'Verdana,10'

set style fill pattern border

set datafile separator ","

set xlabel "x - instance number"
set ylabel "y - time(s) x 10.000"

set title "Connection Time Non Auth"

set output 'nonauth_connection.png'

plot 'logs/20191205_amqp_publish_non_auth.csv' using 3 with boxes title "AMQP",\
     'logs/20191205_mqtt_publish_non_auth.csv' using 3 with boxes title "MQTT",\
     'logs/20191205_stomp_publish_non_auth.csv' using 3 with boxes title "STOMP"

set title "Connection Time Auth"

set output 'auth_connection.png'

plot 'logs/20191205_amqp_publish_auth.csv' using 3 with boxes title "AMQP",\
     'logs/20191205_mqtt_publish_auth.csv' using 3 with boxes title "MQTT",\
     'logs/20191205_stomp_publish_auth.csv' using 3 with boxes title "STOMP"

set title "Publish Time"

set output 'non_publish.png'

plot 'logs/20191205_amqp_publish_non_auth.csv' using 4 with boxes title "AMQP",\
     'logs/20191205_mqtt_publish_non_auth.csv' using 4 with boxes title "MQTT",\
     'logs/20191205_stomp_publish_non_auth.csv' using 4 with boxes title "STOMP"
