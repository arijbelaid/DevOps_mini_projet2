FROM nginxinc/nginx-unprivileged:1.25-alpine

# C'est CETTE ligne qui manque sûrement !
COPY default.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 8080