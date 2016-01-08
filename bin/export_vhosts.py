##################################################################################################
#
# script para exportar configuraci√n de virtual host a archivo .ini
#
#
# Recibe como parametro:
# 0 = archivo ini con el listado de vhosts a exportar
# 1 = directorio properties donde se creara el archivo con la configuracion
#
# By: Luis Ramirez Q.
# 3HTP
# lramirez@3htp.com
#
#################################################################################################

import sys
import time
import ConfigParser
import commands
import os
import com.ibm.ws.scripting.ScriptingException

##############################################################################################
# Definicion metodos
###############################################################################################

#Metodo hora actual para logs
def hora_actual():
	return  "["+time.strftime('%x')+" "+time.strftime('%X') + "] "

#metodo que permite escribir la configuracion a un archivo
def details(vh):
	print hora_actual() + " ======[" + vh + "]================================================"
	#AdminConfig.show(vh).split('\n')
	name = AdminConfig.showAttribute(vh,'name')
	
	try:
		name=cfg.get(name, 'name_target')
	except:
		print hora_actual() + " No tiene name target asociado"
	print hora_actual() + "name_target = " + name

        my_file.write("["+name+"] \n")
	#se obtienen los mimes types asociados
#	mimes = AdminConfig.showAttribute(vh, 'mimeTypes').split(" ")


	#se obtienen los host alias asociados al virtual hosts
	aliases = AdminConfig.showAttribute(vh, 'aliases').split(" ")
	
	#se obtiene el listado de virtual alias asociado al virtual hosts y se escribe en el archivo .ini
	for i  in range(len(aliases)):
		x =  aliases[i] 
		a = x.replace("[","")
		b = a.replace("]","")
		try:
			hostname=AdminConfig.showAttribute(b,'hostname')
			port=AdminConfig.showAttribute(b, 'port')
			print hora_actual() + " hostname " + hostname + " port " + port 
			my_file.write("hostname" +str(i) + "="+hostname+"\n")
			my_file.write("port"+str(i)+"="+port+"\n")
		except:
			print hora_actual() + " Error al resolver Alias para virtual host [" + name + "]"
#========================================================
# inicio script
#====================================================
#read parametros
if len(sys.argv) != 2:
        print hora_actual() + "Error: argumentos invalidos"
        sys.exit(1)

file_conf=sys.argv[0]
folder_properties=sys.argv[1]

print hora_actual() + "=============================================================="
print hora_actual() + "folder_properties : " + folder_properties
print hora_actual() + "file_conf : " + file_conf
print hora_actual() + "=============================================================="

	
#crear archivo con configuracion exportada	
my_file = open(folder_properties+'/vhost_export.ini','w')

#leer archivo de propiedades
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo vhosts.ini"
	sys.exit(1)
	
#get list virtualhosts from file ini
vhs = cfg.sections()

#get list id virtual hosts
all_vhs = AdminConfig.list('VirtualHost').split('\n')

#por cada virtual hosts realizamos el export
for vh_name in vhs:
	for vh in all_vhs:
		if vh_name == AdminConfig.showAttribute(vh,'name'):
			details(vh)



#close file config 
my_file.close()
