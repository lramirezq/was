#########################################################################################
# Script exporta DataSources 
###########################################################################################
import sys
import os
import time
import ConfigParser
import commands
import com.ibm.ws.scripting.ScriptingException

def details_datasource(datasource):
	try:
		print "================================================================================================="
		name = AdminConfig.showAttribute(datasource, 'name')
		authMechanismPreference =  AdminConfig.showAttribute(datasource, 'authMechanismPreference')
		connectionPool = AdminConfig.show(AdminConfig.showAttribute(datasource, 'connectionPool'))
		datasourceHelperClassname = AdminConfig.showAttribute(datasource, 'datasourceHelperClassname')+ "]"
		description = AdminConfig.showAttribute(datasource, 'description')
		diagnoseConnectionUsage = AdminConfig.showAttribute(datasource, 'diagnoseConnectionUsage')
		jndiName = AdminConfig.showAttribute(datasource, 'jndiName')
		logMissingTransactionContext = AdminConfig.showAttribute(datasource, 'logMissingTransactionContext')
		manageCachedHandles = AdminConfig.showAttribute(datasource, 'manageCachedHandles')
		statementCacheSize = AdminConfig.showAttribute(datasource, 'statementCacheSize')
		properties = AdminConfig.showAttribute(datasource, 'properties')
		relationalResourceAdapter = AdminConfig.showAttribute(datasource, 'relationalResourceAdapter')
		try:
			agedTimeout = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'agedTimeout')
			connectionTimeout = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'connectionTimeout')
			freePoolDistributionTableSize = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'freePoolDistributionTableSize')
			maxConnections = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'maxConnections')
			minConnections = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'minConnections')
			numberOfFreePoolPartitions = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'numberOfFreePoolPartitions')
			numberOfSharedPoolPartitions = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'numberOfSharedPoolPartitions')
			numberOfUnsharedPoolPartitions = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'numberOfUnsharedPoolPartitions')
			properties = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'properties')
			purgePolicy = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'purgePolicy')
			reapTime = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'reapTime')
			stuckThreshold = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'stuckThreshold')
			stuckTime = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'stuckTime')
			stuckTimerTime = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'stuckTimerTime')
			surgeCreationInterval = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'surgeCreationInterval')
			surgeThreshold = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'surgeThreshold')
			testConnection = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'testConnection')
			testConnectionInterval = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'testConnectionInterval')
			unusedTimeout = AdminConfig.showAttribute(AdminConfig.showAttribute(datasource, 'connectionPool'), 'unusedTimeout')
			
			
			



			
		except:
			print "error al hacer get "
		my_file.write("["+name+"] \n")
		my_file.write("authMechanismPreference=" +authMechanismPreference+"\n")
		my_file.write("datasourceHelperClassname=" +datasourceHelperClassname+"\n")
		my_file.write("description=" + description +"\n")
		my_file.write("diagnoseConnectionUsage=" +diagnoseConnectionUsage+"\n")
		my_file.write("jndiName=" +jndiName+"\n")
		my_file.write("logMissingTransactionContext=" +logMissingTransactionContext+"\n")
		my_file.write("manageCachedHandles=" +manageCachedHandles+"\n")
		my_file.write("statementCacheSize=" +statementCacheSize+"\n")
		my_file.write("properties=" +properties+"\n")
		my_file.write("relationalResourceAdapter=" +relationalResourceAdapter+"\n")
		#agrega detalle de connection pool
		my_file.write("connectionPool.agedTimeout="+agedTimeout+"\n") 
		my_file.write("connectionPool.connectionTimeout="+connectionTimeout+"\n")
		my_file.write("connectionPool.freePoolDistributionTableSize="+freePoolDistributionTableSize+"\n")
		my_file.write("connectionPool.maxConnections="+maxConnections+"\n")
		my_file.write("connectionPool.minConnections="+minConnections+"\n")
		my_file.write("connectionPool.numberOfFreePoolPartitions="+numberOfFreePoolPartitions+"\n")
		my_file.write("connectionPool.numberOfSharedPoolPartitions="+numberOfSharedPoolPartitions+"\n")
		my_file.write("connectionPool.numberOfUnsharedPoolPartitions="+numberOfUnsharedPoolPartitions+"\n")
		my_file.write("connectionPool.properties="+properties+"\n")
		my_file.write("connectionPool.purgePolicy="+purgePolicy+"\n")
		my_file.write("connectionPool.reapTime="+reapTime+"\n")
		my_file.write("connectionPool.stuckThreshold="+stuckThreshold+"\n")
		my_file.write("connectionPool.stuckTime="+stuckTime+"\n")
		my_file.write("connectionPool.stuckTimerTime="+stuckTimerTime+"\n")
		my_file.write("connectionPool.surgeCreationInterval="+surgeCreationInterval+"\n")
		my_file.write("connectionPool.surgeThreshold="+surgeThreshold+"\n")
		my_file.write("connectionPool.testConnection="+testConnection+"\n")
		my_file.write("connectionPool.testConnectionInterval="+testConnectionInterval+"\n")
		my_file.write("connectionPool.unusedTimeout="+unusedTimeout+"\n")
		
		#propertySet [" + AdminConfig.show(AdminConfig.showAttribute(datasource, 'propertySet'))+ "]"
		#mapping [" + AdminConfig.show(AdminConfig.showAttribute(datasource, 'mapping'))+ "]"
	except:
		print "algunas propiedades no se encontraron"
	
	


	
	
#================================================
#
#
#================================================
my_file = open('/home/temporal/3htp/properties/datasources.ini','w')
datasources = AdminConfig.list('DataSource').split('\n')
for datasource in datasources:
	details_datasource(datasource)
my_file.close()