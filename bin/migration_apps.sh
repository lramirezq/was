#!/bin/sh

#load properties to session

. ../properties/config.properties
  
# Read properties
echo "path profile: [$dmgr_was_source]"
echo "user was    : [$user_was_source]"
echo "conf app 	  : [$conf_app]"
echo "=========================================================="

#clean repository directory
echo "Repository directory is [$repository_source]"
sudo rm -rf $repository_source/*
echo "Reposity directory is clean"
echo "=========================================================="
#export app to filesystem
echo "Starting export of apps to filesystem"
sudo $dmgr_was_source/bin/wsadmin.sh -username $user_was_source -password $pass_was_source -lang jython -f export_app.py $repository_source $conf_app
wait
echo "=========================================================="

#clean repository target
echo "Clean directory work target"

echo  "Repository directory work target [$work_dir_target]"
#ssh $ip_target "rm -rf $work_dir_target"

echo "=========================================================="
#copy ear to target
echo "Copying  config and EAR to targer"
#scp -r $work_dir_source $ip_target:$work_dir_target
echo "Se han copiado los EAR correctamente"
echo "=========================================================="

echo "instalar aplicacion en destino"
#ssh $ip_target "cd $work_dir_target/bin && sudo $dmgr_was_target/bin/wsadmin.sh -username $user_was_target -password $pass_was_target -lang jython -f install_app.py $repository_target $conf_app"
wait
echo "Se instalo en destino"
