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
echo "Installing postgis and gdal-bin: apt-get install postgis gdal-bin -y"
sudo apt-get install postgis gdal-bin -y
echo "################################################################################"
echo "Installing apache2"
sudo apt-get install apache2
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
sudo apt-get install npm sass
echo "################################################################################"
