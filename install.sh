#!/bin/bash

sudo apt install python3-pip
sudo apt install autoconf
sudo apt install autogen
sudo apt install libtool
sudo apt install swig
sudo apt install libffi-dev
sudo apt install libssl-dev
sudo apt install make swig meson cmake zsh gcc
curl https://sh.rustup.rs -sSf | sh
python -m pip install --upgrade pip
pip install --upgrade poetry
source ~/.profile && source "$HOME/.cargo/env" && poetry add  ./external_packages_armv7/zenroom-2.1.0.dev1655293214-cp39-cp39-linux_armv7l.whl
source ~/.profile && poetry install
