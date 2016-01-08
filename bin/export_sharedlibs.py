#########################################################################################
# Script exporta configuración de shared lib a un archivo ini
# parametros de entrada
# 1) archivo ini 
# 2) path folder bin
# 3) usuario
###########################################################################################

import sys
import os
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

#Metodo hora actual para logs
def hora_actual():
	return  "["+time.strftime('%x')+" "+time.strftime('%X') + "] "

#metodo para devolver el valor de una variable	
def valueVar(find):
	cell = AdminConfig.list("Cell")
	cellName = AdminConfig.showAttribute(cell, "name")
	cellWebSphereVariableMap = AdminConfig.getid("/Cell:"+cellName+"/VariableMap:/")
	cellEntries = AdminConfig.list('VariableSubstitutionEntry').split("\n")
	value = ''
	for entry in cellEntries:
		#print "id : ["  + entry + "]"
		try:
			name = AdminConfig.showAttribute(entry, "symbolicName")
			v = AdminConfig.showAttribute(entry, "value")
			#print "[" + name +"] == [" +find+"]" 
			if name == find:
				value = v
		except:
			print "ERROR BUSCANDO VALOR PARA VARIABLE [" + find +"]"
		
	return value
	
#Metodo que ejecuta un script shell que tiene la lógica para copiar archivos al destino
def copy_to_target(f):
	print "[" + f +"]"
	try:
		varname = f.split('${', 1)[1].split('}')[0];
		file  = f.replace("${"+varname+"}", valueVar(varname))
	except:
		file = f
	os.system("su "+ usuario+ " -c sh "+ folder_bin +"/copy_file.sh " +file+" " +host_destino)
	
#=====================================
# Inicio
#======================================
def export_lib(lib):
	#print "=================================="
	#print "a crear en archivo [" + lib + "]"
	name = AdminConfig.showAttribute(lib,'name')
	c = AdminConfig.showAttribute(lib,'classPath')
	try:
		varname = c.split('${', 1)[1].split('}')[0];
		classpath  = c.replace("${"+varname+"}", valueVar(varname))
	except:
		classpath = c
	isolatedClassLoader = AdminConfig.showAttribute(lib,'isolatedClassLoader')
	nativePath= AdminConfig.showAttribute(lib,'nativePath')
	#print "Name Libs [" + name +"]"
	#print "classpath Libs [" + classpath +"]"
	my_file.write("["+name+"] \n")
	my_file.write("classpath=" + classpath +"\n")
	my_file.write("isolatedClassLoader=" +isolatedClassLoader+"\n")
	my_file.write("nativePath="+nativePath+"\n")
	#print "=================================="
	#print "Lista de jars de classpath"
	print hora_actual() + "Libreria a Migrar [" + name + "]"
	classpaths =  classpath.split(';')
	#copiar archivos al destino
	for c in classpaths:
		copy_to_target(c)
##################################################################################
# inicio script
###################################################################################	

#read parametros
if len(sys.argv) != 5:
        print hora_actual() + "Error: argumentos invalidos"
        sys.exit(1)

usuario = sys.argv[0]
folder_properties=sys.argv[1]
folder_bin=sys.argv[2]
file_conf=sys.argv[3]
host_destino=sys.argv[4]

print hora_actual() + "=============================================================="
print hora_actual() + "Usuario : " + usuario
print hora_actual() + "folder_properties : " + folder_properties
print hora_actual() + "folder_bin : " + folder_bin
print hora_actual() + "file_conf : " + file_conf
print hora_actual() + "host_destino : " + host_destino
print hora_actual() + "=============================================================="

	
#crear archivo con configuracion exportada	
my_file = open(folder_properties+'/sharedlibs_export.ini','w')

#leer archivo de propiedades
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo sharedlibs.ini"
	sys.exit(1)
	
#get applications
libs = cfg.sections()
all_libs = AdminConfig.list('Library').split('\n')

#se exportan todas las libs
if  len(libs) < 2:
	for lib in all_libs:
		if lib != "default_config":
			export_lib(lib)
#se importan solo las del archivo
else:
	#por cada aplicacion realizamos el export
	for lib_name in libs:
		for lib in all_libs:
			if lib_name == AdminConfig.showAttribute(lib,'name'):
				export_lib(lib)
		
		
#cierro archivo	
my_file.close()