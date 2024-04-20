FROM node:20-bullseye

WORKDIR /frontend

COPY ./frontend/react/package.json /frontend/
COPY ./frontend/react/package-lock.json /frontend/

RUN npm install npm@latest && npm install

COPY . /frontend/