#!/bin/bash

sudo apt install python3-pip
sudo apt install autoconf
sudo apt install autotools
sudo apt install autogen
sudo apt install libtool
sudo apt install swig
sudo apt install libffi-dev
sudo apt install libssl-dev
sudo apt install make swig meson cmake zsh gcc
python -m pip install --upgrade pip
pip install --upgrade pipenv
pip install --upgrade poetry


poetry add  ./external_packages_armv7/zenroom-2.1.0.dev1655293214-cp39-cp39-linux_armv7l.whl
poetry install
