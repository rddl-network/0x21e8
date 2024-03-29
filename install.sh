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
#install libwallycore on your system
apt-get install -y curl bash
apt-get install -y make meson cmake zsh gcc git
git clone https://github.com/ElementsProject/libwally-core.git
cd libwally-core/
git checkout release_0.8.6
git submodule init
git submodule sync --recursive
git submodule update --init --recursive
./tools/autogen.sh
PYTHON_VERSION=3.9 ./configure --enable-debug --enable-export-all --enable-swig-python && \
    make && make install
cd ..
#source ~/.profile && source "$HOME/.cargo/env" && PIP_NO_BINARY="zenroom" poetry add zenroom
source ~/.profile && source "$HOME/.cargo/env" && poetry add  ./external_packages_armv7/zenroom-2.3.4-cp39-cp39-linux_armv7l.whl
source ~/.profile && poetry install
