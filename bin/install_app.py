#########################################################################################
# 
# Script que permite instalar/actualizar  aplicaciones desde un repositorio
# scope = Cluster
#
# parametros:
# arg[0] : repository local 
# arg[1] : archivo de configuracion, detalle de aplicaciones a export
#
# By: Luis Ramirez Queupul
# 3HTP
# lramirez@3htp.com
###########################################################################################

import sys
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

##############################################################################################
# Definicion metodos
##############################################################################################
#Metodo hora actual para logs
def hora_actual():
	return  "["+time.strftime('%x')+" "+time.strftime('%X') + "] "

def isAppExists(app):
	return len(AdminConfig.getid("/Deployment:" + app + "/" )) > 0
	
def options_intall(app, vh, cluster, cellName, nodeName, serverName):
	#read nombre con que se instalara la aplicacion en el destino
	try:
		appname = cfg.get(app, 'name_target')
	except:
		appname = app

	options = ['-nopreCompileJSPs',
		'-distributeApp',
		'-nouseMetaDataFromBinary',
		'-nodeployejb',
		'-createMBeansForResources',
		'-noreloadEnabled',
		'-nodeployws',
		'-validateinstall warn',
		'-noprocessEmbeddedConfig',
		'-filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755',
		'-noallowDispatchRemoteInclude',
		'-noallowServiceRemoteInclude',
		'-appname', appname,
		'-cluster', cluster,
		'-MapWebModToVH', [['.*', '.*', vh]],
		'-MapModulesToServers', [['.*', '.*', '+WebSphere:cell='+cellName+',node='+nodeName+',server='+serverName+'+WebSphere:cell='+cellName+',cluster='+cluster]]
	]
	return options	
 

#metodo para instalar o actualizar una aplicacion sobre un cluster
def install_app_cluster(app):
	#get cell
	cells = AdminConfig.list('Cell').split("\n")
	for cell in cells:
		cellName=AdminConfig.showAttribute(cell, 'name')
    #get nodename
	objNameString = AdminControl.completeObjectName('WebSphere:type=Server,*') 
	nodeName = AdminControl.getAttribute(objNameString, 'nodeName')
	
	print hora_actual() + "=========== Comienza la instalacion de: [" + app + "] ========================"
	c = ""
	r = 0
	vh = ""
	webserver = ""
	#read properties from file ini
	print hora_actual() + "=========== Leyendo parametros desde archivo INI ====================="
	try:
		webserver = cfg.get(app,"webserver")
	except:
		try:
			webserver = cfg.get("default_config", "webserver")
		except:
			print hora_actual() +  "Propiedad [webserver] no encontrada en archivo ini"

	try:
		c = cfg.get(app,"cluster")
	except:
		try:
			c = cfg.get("default_config", "cluster")
		except:
			print hora_actual() +  "Propiedad [cluster] no encontrada en archivo ini"

	try:
		vh = cfg.get(app,"virtual_host")
	except:
		try:
			vh = cfg.get("default_config","virtual_host")
		except:
			print hora_actual() + "Propiedad [virtual_host] no encontrada en archivo ini"

	print hora_actual() + "=========== Comienza la instalacion de: [" + app + "] Cluster ["+c+"]========================"
	
	
	#si existe app update elseif install


	try:
		if c != "" and vh != "" and webserver != "":
			if isAppExists(app):
				print "Applicacion Existe"
				AdminApp.update(app, 'app', '[ -operation update -contents '+ repository+'/'+app+'.ear]');
				AdminConfig.save()
			else:
				print "aplicacion no existe"
				AdminApp.install(repository+"/"+app+".ear", options_intall(app, vh, c, cellName, nodeName, webserver))
				AdminConfig.save()
			
		else:
			print hora_actual() + "ERROR : NO SE HA ESPECIFICADO CLUSTER, WEBSERVER O VIRTUAL HOST DE DESTINO PARA LA APLICACION"
	except:
			print hora_actual() + "ERROR : AL INSTALAR LA APLICACION "
	
	print hora_actual() + "=========== fin de instalación la instalacion de: [" + app + "] ========================"

	
	

#############################################################################################
#  Inicio Script
##############################################################################################

print hora_actual() + "starting script for install / update apps"

#recibo argumentos desde la shell principal, se valida que vengan 2 parametros
if len(sys.argv) != 2:
        print hora_actual() + "Error: argumentos invalidos"
        sys.exit(1)

repository = sys.argv[0]
file_conf=sys.argv[1]

print hora_actual() + "repositorio target : " + repository
print hora_actual() + "file config target : " + file_conf	
print hora_actual() + "Starting reading properties"
cfg = ConfigParser.ConfigParser()
try:
	cfg.read([file_conf])
except:
	print hora_actual() + "Error al buscar archivo applications.ini"
	sys.exit(1)
	
#get applications
aplicaciones = cfg.sections()

#por cada aplicacion realizamos el export
for app in aplicaciones:
	if app != "default_config":
		install_app_cluster(app)
	
