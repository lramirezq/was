import sys

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
			print "siga"
		
	return value	
	
#call function

classpath='${WAS_INSTALL_ROOT}/derby/lib/derby.jar'
print "a pasar [" +classpath+"]"
varname = classpath.split('${', 1)[1].split('}')[0];
  
print "[" + varname + "]"

va1 = classpath.replace("${"+varname+"}", valueVar(varname))
print "[" + va1  + "]"
