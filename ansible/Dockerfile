FROM alpine:3.19

# Install Ansible Core, Docker CLI, curl, and python3
RUN apk add --no-cache ansible-core docker-cli curl python3

WORKDIR /workspace

CMD ["ansible-playbook", "--version"]
