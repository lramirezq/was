############################################
## Script para crear JDBC Providers 
#
#
# By: Luis Ramirez Queupul
# 3HTP
# lramirez@3htp.com
#
###########################################

import sys
import os
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

#Metodo hora actual para logs
def hora_actual():
    return  "["+time.strftime('%x')+" "+time.strftime('%X') + "]"


#metodo para crear jdbc provider  en servidor
def create_provider(provider):
	print hora_actual() + "=============== [" + provider + "] ===================="
	#obtener info de cell
	cells = AdminConfig.list('Cell').split("\n")
	for cell in cells:
		cellName=AdminConfig.showAttribute(cell, 'name')
	#se crea provider 
	n = ""
	ic = ""
	icl = ""
	pt = ""
	x = ""
	try:
		n = provider
		print "n = " + n
		ic = cfg.get(provider, 'implementationClassName')
		print "ic " + ic
		icl = cfg.get(provider, 'isolatedClassLoader')
		print "icl " + icl
		pt = cfg.get(provider, 'providerType')	
		print "pt " + pt
		x = cfg.get(provider, 'xa')
		print "x " + x
		c = cfg.get(provider, 'classpath')
	except:
		print "algunas propiedades no se encuentran"

	name = ['name', n]
	implementationClassName = ['implementationClassName', ic]
	isolatedClassLoader = ['isolatedClassLoader', icl]
	providerType = ['providerType', pt]
	xa = ['xa', x]
	classpath = ['classpath', c]
	jdbcAttrs = [name, implementationClassName, isolatedClassLoader,  providerType, xa, classpath]
	print jdbcAttrs
	#create JDBCProvider
	try:
		AdminConfig.create('JDBCProvider', cell, jdbcAttrs)
		AdminConfig.save()
	except Exception:
		print "ERROR AL CREAR"
	
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
    print hora_actual() + "Error al buscar archivo providers_export.ini"
    sys.exit(1)

providers = cfg.sections()
#iterar sobre lista de virtual hostsi

if len(providers) > 0:
	for provider in providers:
    		create_provider(provider)
else:
	print hora_actual() + "No existen providers  en archivo para crear"
