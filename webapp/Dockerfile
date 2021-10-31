FROM node:16
# Install apt dependencies
RUN apt update

# Install requirements
COPY . /app
WORKDIR /app
RUN npm install
EXPOSE 5500
ENTRYPOINT npm start