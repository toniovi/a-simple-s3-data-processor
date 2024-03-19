# List of python devcontainer images here: https://github.com/devcontainers/images/tree/main/src/python
FROM python:3.11-bookworm

WORKDIR /app
COPY . .

# Install Docker 
RUN apt-get update -y && apt-get install -y ca-certificates curl gnupg \
    && install -m 0755 -d /etc/apt/keyrings  \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update
RUN VERSION_STRING=5:24.0.7-1~debian.12~bookworm && \
    apt-get install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin

# Install task and launch the installation task
RUN chmod +x .infra/assets/task_install.sh && sh .infra/assets/task_install.sh -d -b /usr/local/bin
RUN task install

# The next line tells the container what to do when created
# Important it stays a simple CMD (and not ENTRYPOINT or other): the compose.yaml that serves as base for the devcontainer config
# bypasses this CMD with 'sleep infinity', which is necessary for Devcontainers to function properly
CMD python src/main.py

EXPOSE 8080
