FROM ollama/ollama

# Install curl and dos2unix
RUN apt-get update && apt-get install -y curl dos2unix

# Copy and make the startup script executable
COPY ollama-init.sh /ollama-init.sh
RUN dos2unix /ollama-init.sh && chmod +x /ollama-init.sh

# RUN ls -l /ollama-init.sh

ENTRYPOINT ["/ollama-init.sh"]
