# Use official Node.js image
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Install netcat for DB readiness check
RUN apt-get update && apt-get install -y netcat-openbsd

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
