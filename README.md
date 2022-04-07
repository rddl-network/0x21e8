# 0x21e8


## Roadmap

1.  wallet with mnemonic phrase (initially host based)
    1.  inlcude hw wallet 
    2.  lua code                - done (using cython now)
    3.  c-lib to do so          - done
2.  deriving issuer wallet from mnemonic phrase for
    1.  liquid                  - done
    2.  planetmint              - done
3.  derive benefiery wallets for
    1.  liquid
    2.  planetmint
4.  create simple UI with QT 
    1.  present link to assets on
        1.  planetmint
        2.  liquid
5.  connect wallet
6.  web ui for external usage


Ile UI
commit zenroom fixes on planetmint

## Prepare the environment
```bash
sudo apt install pipenv
pipenv install -r requirments.txt
pipenv install git+ssh://git@github.com/riddleandcode/wallet2.git@trezor_crypto_cython#subdirectory=crypto&egg=trezorcrypto_1.0.0 
```


## running the development service
```bash
cd 0x21e8 # that's the folder where main.py is located within
uvicorn --log-level debug --reload main:app
```


