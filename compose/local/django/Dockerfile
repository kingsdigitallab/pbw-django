FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # curl for node
  && apt-get install -y curl \
  # mysql dependencies
  && apt-get install -y default-libmysqlclient-dev \
  #&& apt-get install -y python-mysqldb python-dev
  # ldap depedndencies
  && apt-get install -y libldap2-dev libsasl2-dev ldap-utils
  #&& apt-get install -y libxml2-dev libxslt-dev python-dev \
  #&& apt-get install -y python3-lxml \
  #gdal libraries
  #&& apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /app
COPY requirements.txt /app
COPY ddhldap/requirements.txt /app/ddhldap/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
