From ubuntu:18.04

MAINTAINER italogsfernandes "https://github.com/italogsfernandes"

# Install dependencies
RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get install -y --force-yes git postgis gdal-bin

# Install apache and write hello world message
RUN echo 'Hello World!' > /var/www/html/index.html

# Configure apache
RUN echo '. /etc/apache2/envvars' > /root/run_apache.sh
RUN echo 'mkdir -p /var/run/apache2' >> /root/run_apache.sh
RUN echo 'mkdir -p /var/lock/apache2' >> /root/run_apache.sh
RUN echo '/usr/sbin/apache2 -D FOREGROUND' >> /root/run_apache.sh
RUN chmod 755 /root/run_apache.sh

EXPOSE 80

CMD /root/run_apache.sh

# Git clone
# RUN cd /home/italo/imagens-medicas-2/im2webapp; python manage.py runserver
# RUN git clone https://github.com/italogsfernandes/imagens-medicas-2 /home/italo/imagens-medicas-2
