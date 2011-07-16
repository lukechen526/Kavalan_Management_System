#!/bin/bash

#The script assumes that a site virtualenv has been created somewhere, such as /opt/webapps/domain.com. The Django project resdies
#in the same directory, e.g. /opt/webapps/domain.com/Kavalan_Management_System

#cd to the site directory and mkdir
cd /opt/webapps/domain.com
mkdir static
mkdir uploads
mkdir scripts

#copy django.wsgi
cp ./Kavalan_Management_System/deployment_configs_scripts/django.wsgi ./scripts

#copy and enable Apache and Nginx configs
cp ./Kavalan_Management_System/deployment_configs_scripts/domain-apache.conf /etc/apache2/sites-available
sudo a2ensite domain-apache.conf

cp ./Kavalan_Management_System/deployment_configs_scripts/domain-nginx.conf /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/domain-nginx.conf /etc/nginx/sites-enabled/domain-nginx.conf


#copy nginx config

#Setup Django
source ./bin/activate
cd ./Kavalan_Mangement_System
sudo chmod a+x ./manage.py

#Compile locale files
./manage.py compilemessages

#Collect static files
./manage.py collectstatic

#Compile Sphinx documentation
cd documentation
sudo sphinx-build -b html ./source ./build


