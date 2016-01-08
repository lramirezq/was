#!/bin/sh
#recibo 
# -archivo a copiar
# host destino 
# 

file=$1
host_target=$2
echo "======================================================================"
echo "archivo a copiar  [$file]"
echo "destino 			[$host_target]"
echo "Se inicia copia de archivo"
#get directory name
directorio=`dirname $file`
#get filename
nombre=`basename $file`

#creo directorio en servidor remoto
ssh $host_target "sudo mkdir -p $directorio"
#copio el archivo al /tmp destino

scp $file $host_target:/tmp
#muevo el archivo en el destino
ssh $host_target "sudo mv /tmp/$nombre $directorio"
echo "Archivo copiado exitosamente"

