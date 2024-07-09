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
  && apt-get install -y libldap2-dev libsasl2-dev ldap-utils \
  #&& apt-get install -y libxml2-dev libxslt-dev python-dev \
  #&& apt-get install -y python3-lxml \
  #gdal libraries
  && apt-get install -y binutils libproj-dev gdal-bin \
    # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app
COPY ddhldap/requirements.txt /app/ddhldap/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY --chown=django:django ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
COPY --chown=django:django . /app


#RUN python manage.py migrate
#RUN python manage.py collectstatic --noinput
#RUN python manage.py build_solr_schema --configure-directory=/app/solr_config/config


# fix solr 8 issue
# docker cp ./solr/conf e7ee989cee93:/var/solr/data/pbw
# docker cp ./solr/solr_backend.py f57deb978d4b:/usr/local/lib/python3.6/site-packages/haystack/backends/
#COPY ./solr/solr_backend.py /usr/local/lib/python3.6/site-packages/haystack/backends/