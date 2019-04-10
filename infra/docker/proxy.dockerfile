# Assets Container
FROM 3lpsy/bountydns-webui:latest as build-stage
WORKDIR /webui

ENV VUE_APP_API_BASE="http://localhost:8080"
ENV VUE_APP_API_URL="http://localhost:8080/api/v1"
ENV VUE_APP_BROADCAST_BASE="http://localhost:8080"
ENV VUE_APP_BROADCAST_URL="ws://localhost:8080/broadcast"

RUN npm run build

# Main Container
FROM nginx:1.15

# do not listen on 80 & 443, a future http service will listen on that port
EXPOSE 8080
EXPOSE 8443

ENV DOMAIN="127.0.0.1:8080"
ENV SSL_LISTEN_PORT="8443"
ENV INSECURE_LISTEN_PORT="8080"
ENV SSL_ENABLED="1"
ENV API_BACKEND_PROTO="https"
ENV API_BACKEND_HOST="api"
ENV API_BACKEND_PORT="8080"
ENV DEBUG_CONF="0"

# for development, make /var/www/nginx/webui a volume
RUN mkdir /nginxconfs
COPY insecure.nginx.conf /nginxconfs

# TODO: make prod actually prod
COPY ssl.nginx.conf /nginxconfs

RUN chown -R nginx:nginx /nginxconfs

RUN mkdir -p /var/www/app
COPY --from=build-stage /webui/dist/ /var/www/app/webui
COPY --from=build-stage /landing/ /var/www/app/landing

RUN chown -R nginx:nginx /var/www

# dynamically configure configs or user defaults to avoid mounts
COPY ./docker-run.sh /usr/bin/docker-run.sh
RUN chmod +x /usr/bin/docker-run.sh
ENTRYPOINT ["/usr/bin/docker-run.sh"]
