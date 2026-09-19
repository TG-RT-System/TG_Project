# See here for image contents: 
# https://github.com/microsoft/vscode-dev-containers/tree/v0.241.1/containers/ubuntu/.devcontainer/base.Dockerfile

# ARG VARIANT="jammy"
# ARG VARIANT="noble"
ARG VARIANT="resolute"
FROM mcr.microsoft.com/devcontainers/base:${VARIANT}

SHELL ["/bin/bash", "-c"]

RUN apt-get update --fix-missing

RUN apt-get -y install --no-install-recommends --fix-missing \
        gcc gdb bear cmake make ninja-build git \
        python3 python3-pip

RUN pip3 install --break-system-packages numpy pandas flask

# Set environment variables
# ENV LLVM_HOME=/root/llvm-project
# ENV PATH=${PATH}:${LLVM_HOME}/bin

RUN echo "set completion-ignore-case on" >> /etc/inputrc

# sudo docker build -t dag-scheduler-docker:latest -f .devcontainer/Dockerfile .
# sudo docker run -i -d --name dag-scheduler -v /home/fyj/3_TOOLS/dag-scheduler:/root/dag-schedule:rw dag-scheduler-docker:latest
# sudo docker exec -it dag-scheduler /bin/bash

# sudo docker start dag-scheduler
# sudo docker stop dag-scheduler
# sudo docker rm dag-scheduler
# sudo docker rmi dag-scheduler-docker:latest
