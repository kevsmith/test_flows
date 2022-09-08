FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y

RUN apt-get -y install inetutils-ping inetutils-telnet \ 
    build-essential fish curl git vim sudo python3 golang \
    python3-pip python3-pip-whl tmux

RUN pip3 install --upgrade pip

RUN useradd -m -G sudo -s /usr/bin/fish debug

USER debug
WORKDIR /home/debug

COPY --chown=root:root files/debug_sudo /etc/sudoers.d/debug_sudo

COPY --chown=debug:debug files/config/ .config

RUN mkdir -p /home/debug/repos/go

RUN pip3 install --user --no-warn-script-location virtualenv poetry pipenv

RUN GOPATH=/home/debug/repos/go go install github.com/nats-io/natscli/nats@latest

ENTRYPOINT [ "/usr/bin/tmux" ]