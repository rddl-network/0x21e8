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
source ~/.profile && source "$HOME/.cargo/env" && poetry add  ./external_packages_armv7/zenroom-2.3.4-cp39-cp39-linux_armv7l.whl
source ~/.profile && poetry install
