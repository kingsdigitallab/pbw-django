FROM nginx:stable-alpine

COPY ./compose/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/robots.txt /usr/share/nginx/robots.txt
#COPY ./pbw2011/ /usr/share/nginx/pbw2011/
#RUN chmod -r +x /usr/share/nginx/pbw2011/