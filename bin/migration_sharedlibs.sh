#!/bin/sh

#load properties to session
. ../properties/config.properties
  
# Read properties
echo "=========== Get properties ==============================="
echo "home_script 			: [$home_script]"
echo "folder_properties		: [$folder_properties]"
echo "folder_bin			: [$folder_bin]"
echo "path profile			: [$dmgr_was_source]"
echo "user was    			: [$user_was_source]"
echo "conf app				: [$conf_app]"
echo "config slib 			: [$conf_sharedlibs]"
echo "usuario 	 			: [$usuario]"
echo "destino 	 			: [$ip_target]"

echo "=========================================================="


#export sharedlibs to file ini
echo "Starting export of sharedlibs to file"
sudo $dmgr_was_source/bin/wsadmin.sh -username $user_was_source -password $pass_was_source -lang jython -f export_sharedlibs.py $usuario $folder_properties $folder_bin $conf_sharedlibs $ip_target
wait
echo "=========================================================="

#clean repository target
echo "Clean directory work target"

echo  "Repository directory work target [$work_dir_target]"
ssh $ip_target "rm -rf $work_dir_target"


#copy configs to target
echo "=========================================================="
echo "Copying  config  to targer"
scp -r $work_dir_source $ip_target:$work_dir_target
echo "Se ha copiado la configuracion"
echo "=========================================================="

echo "importar sharedlibs en destino"
file_details=$folder_properties/sharedlibs_export.ini
echo "Archivo con config : [$file_details]"|
ssh $ip_target "cd $work_dir_target/bin && sudo $dmgr_was_target/bin/wsadmin.sh -username $user_was_target -password $pass_was_target -lang jython -f $work_dir_target/bin/import_sharedlibs.py $file_details"
wait
echo "Se importo en destino"

