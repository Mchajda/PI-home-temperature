# Use an official Node.js runtime as the base image
FROM node:16-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Install TypeScript globally
RUN npm install -g typescript

# Copy the rest of the application code to the container
COPY . .

# Build the React app (this will compile TypeScript files)
RUN npm run build

# Install a simple HTTP server to serve static files
RUN npm install -g serve

# Expose port 3000 to be accessible from outside the container
EXPOSE 3000

# Run the application using the HTTP server, serving the built files
CMD ["serve", "-s", "build", "-l", "3000"]
