# Pull base image
FROM python:3.7-alpine

MAINTAINER italogsfernandes "https://github.com/italogsfernandes"

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /home/italo/imagens-medicas-2/im2webapp

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /home/italo/imagens-medicas-2/
RUN pipenv install --system

# Copy project
COPY . /home/italo/imagens-medicas-2/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
