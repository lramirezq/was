############################################################################################
# Script para crear virtual hosts en destino
#
# recibe como parametro un archivo ini con la configuraciÃn de virtual host a crear
#
#
# by: luis ramirez
# 3HTP
# lramirez@3htp.com
###########################################################################################

import sys
import os
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

#Metodo hora actual para logs
def hora_actual():
    return  "["+time.strftime('%x')+" "+time.strftime('%X') + "]"


#metodo para crear vhost en servidor
def create_vh(vh):
	print hora_actual() + "=============== [ " + vh + " ] ===================="
	#obtener info de cell
	cells = AdminConfig.list('Cell').split("\n")
	for cell in cells:
		cellName=AdminConfig.showAttribute(cell, 'name')
	#se crea virtual host
	id_vh = AdminConfig.create('VirtualHost', cell, '[[name '+ vh +']]') 
	AdminConfig.save()
	print hora_actual() + "virtual host creado exitosamente"
	#count iterate
	c = 0
	#control while
	sw = "siga"
	while(sw=="siga"):
		try:
			prop="hostname"+str(c)
			#print "vamos a buscar " + prop
			#get host
			h=cfg.get(vh,prop)
			prop="port"+str(c)
			#get Ã±port
			p=cfg.get(vh,prop)
			#print "host = " + h
			#print "port = " + p

			#create hostalias asociado
			AdminConfig.create('HostAlias', id_vh, '[[port '+p +'] [hostname '+h+']]')
			AdminConfig.save()
			#si todo OK 
			print hora_actual() + "host alias creado exitosamente" 
			#increment count
			c+=1
		except Exception:
			sw= "stop"
		

#==================================================================
# Inicio script
#==================================================================

#read parametros
if len(sys.argv) != 1:
    print hora_actual() + "Error: numero de argumentos invalidos"
    sys.exit(1)

file_conf = sys.argv[0]
print hora_actual() + "el archivo de configuracion que se importara es [" + file_conf + "]"

#leer archivo de configuracion
cfg = ConfigParser.ConfigParser()
try:
    cfg.read([file_conf])
except:
    print hora_actual() + "Error al buscar archivo vhost_export.ini"
    sys.exit(1)

vhs = cfg.sections()
#iterar sobre lista de virtual hostsi

if len(vhs) > 0:
	for vh in vhs:
    		create_vh(vh)
else:
	print hora_actual() + "No existen virtual host en archivo para crear"
