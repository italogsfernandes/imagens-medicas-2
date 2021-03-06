echo "################################################################################"
echo "# sudo mode"
sudo -i
echo "################################################################################"
echo "Updating repositories: apt-get update"
apt-get update
echo "################################################################################"
echo "Upgrating packages: apt-get upgrade -y"
apt-get upgrade -y

echo "################################################################################"
echo "Creating user: $1"
adduser $1
adduser $1 sudo
sudo su $1
sudo hostname italogsfernandes #http://ubuntuhandbook.org/index.php/2014/04/change-hostname-ubuntu1404/
#sudo nano /etc/hostname
#sudo nano /etc/hosts

echo "################################################################################"
echo "SSH"
cd
mkdir .ssh
chmod 700 .ssh
echo "################################################################################"
echo "Authorized Keys"
cd
touch .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
echo "################################################################################"
echo "Paste the clipboard content (the copied id_rsa.pub value): "
cat >> .ssh/authorized_keys

echo "################################################################################"
echo "Firewall allow out deny in"
sudo ufw default allow outgoing
sudo ufw default deny incoming
echo "################################################################################"
echo "Firewall allor ssh, http, flaskdebug and django debug"
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 5000
sudo ufw allow 8000
echo "################################################################################"
echo "Firewall Enable"
sudo ufw enable
echo "################################################################################"
echo "Firewall status: "
sudo ufw status

echo "################################################################################"
echo "Installing postgis and gdal-bin: apt-get install postgis gdal-bin gettext -y"
sudo apt-get install postgis gdal-bin -y
sudo apt-get install gettext -y
echo "################################################################################"
echo "Installing apache2 and mod-wsgi"
sudo apt-get install apache2
# sudo apt-get install libapache2-mod-wsgi
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
echo "################################################################################"
echo "Installing and configuring postgresql"
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser --interactive
sudo adduser italo
echo "################################################################################"


echo "################################################################################"
echo "Virtual env"
sudo apt-get install python3-pip
sudo pip3 install virtualenv
# virtualenv -p python3 env

echo "################################################################################"
echo "Installing npm and sass: sudo apt-get install npm sass
sudo apt-get install npm sass"
echo "################################################################################"


echo "################################################################################"
echo "Step 3: Install Docker"
echo "To install Docker on Ubuntu, in the terminal window enter the command:"
echo "sudo apt install docker.io"
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
docker --version
# sudo docker run -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock v2tec/watchtower
echo "################################################################################"

echo "################################################################################"
echo "Then you need to run the Docker container for your project! (login before)"
echo "################################################################################"
sudo docker login
sudo pip3 install docker-compose

echo "################################################################################"
echo "Project specific"
echo "################################################################################"
echo "Git clone:"
git clone https://github.com/italogsfernandes/server-management.git
echo "Virtual Env:"
virtualenv -p python3 /home/italo/imagens-medicas-2/env
source /home/italo/imagens-medicas-2/env/bin/activate
# virtualenv -p python3 env
# source env/bin/activate
echo "Pip requirements:"
pip3 install -r /home/italo/imagens-medicas-2/requirements.txt
# pip3 install -r requirements.txt

echo "Creating postgresql DB:"
createdb im2webapp
echo "Configuring postgresql to production:"
sudo nano /etc/postgresql/10/main/pg_hba.conf
# Change this line:
# -local   all             all                                     peer
# To this:
# +local   all             all                                     md5
sudo service postgresql restart # I dont know if i need this

echo "Configuring postgresql to production creating user:"
# dropuser <username>
sudo su - postgres
# role and pass in private files
# next 3 questions -> n (do not allow)
createuser --interactive --pwprompt
psql
GRANT italo TO <username>;
\q
exit

# GRANT ALL ON DATABASE im2webapp TO <username>;
# GRANT ALL ON SCHEMA public TO <username>;
# GRANT ALL ON ALL TABLES IN SCHEMA public TO <username>;
# REVOKE ALL ON DATABASE im2webapp FROM <username>;
# REVOKE ALL ON SCHEMA public FROM <username>;
# REVOKE ALL ON ALL TABLES IN SCHEMA public FROM <username>;
# REVOKE italo FROM im2webapp_django_user;

echo "Migrating:"
python /home/italo/imagens-medicas-2/im2webapp/manage.py migrate
echo "Creating super user:"
python /home/italo/imagens-medicas-2/im2webapp/manage.py createsuperuser

echo "compile locale:"
python /home/italo/imagens-medicas-2/im2webapp/manage.py compilemessages

echo "Running first debug: "
python /home/italo/imagens-medicas-2/im2webapp/manage.py runserver 0.0.0.0:8000

echo "WSGI:"
scp wsgi_production.py italo@italogsfernandes.com:/home/italo/imagens-medicas-2/im2webapp/django_project/

echo "Apache2 conf (httpd.conf) + WSGI:"
echo "NOTE: This path can change depending on apache version"
sudo cp /home/italo/imagens-medicas-2/utils/apache2.conf /etc/apache2/apache2.conf
python /home/italo/imagens-medicas-2/im2webapp/manage.py migrate
python /home/italo/imagens-medicas-2/im2webapp/manage.py collectstatic --noinput

sudo service apache2 restart

echo "##################"
echo "env variables"
echo "##################"
sudo nano /etc/environment
