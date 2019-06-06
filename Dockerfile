# Pull base image
FROM python:3.6

MAINTAINER italogsfernandes "https://github.com/italogsfernandes"
ADD . /home/italo/imagens-medicas-2/

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /home/italo/imagens-medicas-2/im2webapp

# Install dependencies
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin postgis
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /home/italo/imagens-medicas-2/

EXPOSE 8000
CMD python manage.py runserver
