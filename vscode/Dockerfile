FROM node:buster as development

# Install git, to ensure the git tools work within vs-code
RUN apt-get update \
    && apt-get install git-all --no-install-recommends -y

WORKDIR /usr/app
COPY ./ /usr/app/

WORKDIR /app
EXPOSE 8008