#########################################################################################
# Script exporta Providers JDBC a file .ini
#
#
# By: Luis Ramirez Queupul
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
	return  "["+time.strftime('%x')+" "+time.strftime('%X') + "] "

#metodo para resolver variables WAS
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

#metodo que obtiene la configuracion del JDBCProviders y la envia a un archivo
def details_provider(provider):
	try:
		print "================================================================================================="
		print "id : [" + provider + "]"

		name = AdminConfig.showAttribute(provider, 'name')
		print "name = " + name
		#classpath = AdminConfig.showAttribute(provider, 'classpath')
		c = AdminConfig.showAttribute(provider,'classpath')
		print "original " + c
		try:
			varname = c.split('${', 1)[1].split('}')[0];
			x =  valueVar(varname)
			#recursivo por si el resultado de la variable contiene otra variable
			while "$" in x:
				varname = c.split('${', 1)[1].split('}')[0];
				y = x.split('${', 1)[1].split('}')[0];
				x  = x.replace("${"+y+"}", valueVar(y))
				print "x = " + x
		
			classpath =  classpath  = c.replace("${"+varname+"}",x)		
				
		except:
			print "ERROR al resolver la variable"
			classpath = c
		print "classpath = " + classpath
		description = AdminConfig.showAttribute(provider, 'description')
		implementationClassName =  AdminConfig.showAttribute(provider, 'implementationClassName')
		isolatedClassLoader = AdminConfig.showAttribute(provider, 'isolatedClassLoader')
		providerType = AdminConfig.showAttribute(provider, 'providerType')
		xa = AdminConfig.showAttribute(provider, 'xa')
		my_file.write("["+name+"] \n")
		my_file.write("classpath=" + classpath +"\n")
		my_file.write("description=" +description+"\n")
		my_file.write("implementationClassName=" + implementationClassName +"\n")
		my_file.write("isolatedClassLoader=" +isolatedClassLoader+"\n")
		my_file.write("providerType=" + providerType +"\n")
		my_file.write("xa=" +xa+"\n")
		
	except:
		print "algunas propiedades no se encontraron"
	
	


	
	
#================================================
# Inicio script
#================================================

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
my_file = open(folder_properties+'/providers_export.ini','w')

#leer archivo de propiedades
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo providers.ini"
	sys.exit(1)
	
#get applications
provs = cfg.sections()
all_provs = AdminConfig.list('JDBCProvider').split('\n')

#por cada aplicacion realizamos el export
for prov_name in provs:
	for prov in all_provs:
		if prov_name == AdminConfig.showAttribute(prov,'name'):
			details_provider(prov)
#close file
my_file.close()
