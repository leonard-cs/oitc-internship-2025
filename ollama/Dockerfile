FROM ollama/ollama

# Install curl so we can wait for the server in the init script
RUN apt-get update && apt-get install -y curl

# Copy and make the startup script executable
COPY ollama-init.sh /ollama-init.sh
RUN chmod +x /ollama-init.sh

# RUN ls -l /ollama-init.sh

ENTRYPOINT ["/ollama-init.sh"]
