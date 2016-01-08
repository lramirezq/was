#########################################################################################
# Script recibe parametros desde shell
# arg[0] : repository local 
# arg[1] : archivo de configuracion, detalle de aplicaciones a export
#
# por cada sección del archivo .inise  genera un export en el origen
# si la seccion tiene definido path_source, realiza una copia desde el path al repository
#
# By: Luis Ramirez Queupul
# 3HTP
# lramirez@3htp.com
#
###########################################################################################

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

#Metodo con logica para export de aplicaciones.
def export_app(app):
	print hora_actual() + "Se comienza a Exportar aplicacion : ["+ app +"]"
	try:
        	#obtengo el path del installer
		try:
			path = cfg.get(app, "path_source")
			print "path : " + path
		except:
			path = ""
		#si tiene path debe copiar el ear a el repositorio
		if path != "":
			os.system("cp "+path+" " + repository)
		else:
			try:
				filename = repository+"/"+app+".ear"
				print "archivo a crear = " + filename
				AdminApp.export(app,filename );
				print hora_actual() + "Export exitoso";
			except Exception:
				print hora_actual() + " ERROR EXPORTANDO APP "
	except Exception:
		print hora_actual() +"Error al Realizar el Export de la aplicacion : ["+ app +"]" 
		#sys.exit(1);
	
#############################################################################################
#  Inicio Script
##############################################################################################
print hora_actual() + "iniciando script for export apps"

#recibo argumentos desde la shell principal, se valida que vengan 2 parametros
if len(sys.argv) != 2:
        print hora_actual() + "Error: argumentos invalidos"
        sys.exit(1)

repository = sys.argv[0]
file_conf=sys.argv[1]

print "repositorio : " + repository
print "file config : " + file_conf
#end read args


print hora_actual() +"backups se generan en : [" + repository +"]"


print hora_actual() + "Read properties"
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo applications.ini"
	sys.exit(1)
	
#get applications
aplicaciones = cfg.sections()
print aplicaciones
aplicaciones.sort()
print aplicaciones
#order acorde a archivo
aplicaciones.reverse()

#por cada aplicacion realizamos el export
for app in aplicaciones:
	if app != "default_config":
		export_app(app)
	
