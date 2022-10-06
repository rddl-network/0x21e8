#!/bin/bash

sudo apt install python3-pip
sudo apt install autoconf
sudo apt install autotools
sudo apt install autogen
sudo apt install libtool
sudo apt install swig
python -m pip install --upgrade pip
pip install --upgrade pipenv

pipenv run pip install pysha3~=1.0.2 python-rapidjson>=1.0.0 python-rapidjson-schema==0.1.1 base58 pynacl==1.4.0 pyasn1 cryptography==3.4.7 requests>=2.20.0 planetmint-cryptoconditions>=0.10.0 TrezorCryptoTestRc planetmint-ipld wallycore==0.8.2 mnemonic fastapi uvicorn
pipenv run pip install planetmint-driver==0.11.1 --no-deps
pipenv run pip install ../dotcode-generator/external_packages_armv7/zenroom-2.1.0.dev1662451250-cp39-cp39-linux_armv7l.whl

