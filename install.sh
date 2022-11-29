#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
sudo apt -y install python3-pip
sudo apt -y install autoconf
sudo apt -y install autogen
sudo apt -y install libtool
sudo apt -y install swig
sudo apt -y install libffi-dev
sudo apt -y install libssl-dev
sudo apt -y install make swig meson cmake zsh gcc
curl https://sh.rustup.rs -sSf | sh
pip install poetry
source ~/.profile && source "$HOME/.cargo/env" && PIP_NO_BINARY="zenroom" poetry add zenroom
source ~/.profile && poetry install
