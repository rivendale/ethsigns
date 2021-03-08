FROM nginx:1.19.0

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
