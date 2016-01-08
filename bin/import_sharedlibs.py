######################################################
# Script para crear libreria compartida en destino
######################################################

import sys
import os
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

#Metodo hora actual para logs
def hora_actual():
	return  "["+time.strftime('%x')+" "+time.strftime('%X') + "]"

def import_lib(lib):
	print hora_actual() + "Se creará la libreria : [" + lib + "]"
	classpath = cfg.get(lib, "classpath")
	isolatedClassLoader= cfg.get(lib, "isolatedClassLoader")
	nativePath= cfg.get(lib, "nativePath")
	print  hora_actual() + "Classpath			 : [" + classpath + "]"
	print  hora_actual() + "isolatedClassLoader  : [" + isolatedClassLoader + "]"
	print  hora_actual() + "nativePath 			 : [" + nativePath + "]"
	#create sharedlib
	#get cell
	cells = AdminConfig.list('Cell').split("\n")
	for cell in cells:
		cellName=AdminConfig.showAttribute(cell, 'name')
		
	#AdminConfig.create('Library', cell, [['name', lib], ['classPath',classpath]]) 
	try:
		AdminConfig.create('Library', cell, [['name', lib], ['classPath', classpath],['isolatedClassLoader', isolatedClassLoader]])
		AdminConfig.save()
		print  hora_actual() + "LIBRERIA CREADA EXITOSAMENTE"
	except:
		print  hora_actual() +	"ERROR AL CREAR LIBRERIA COMPARTIDA : [" + lib + "]"
	
#==================================================================
# Inicio script
#==================================================================

#read parametros
if len(sys.argv) != 1:
        print hora_actual() + "Error: argumentos invalidos"
        sys.exit(1)

file_conf = sys.argv[0]
print hora_actual() + "el archivo de configuracion que se importará es [" + file_conf + "]"

#leer archivo de configuracion
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo sharedlibs_export.ini"
	sys.exit(1)

libs = cfg.sections()
for lib in libs:
	import_lib(lib)
