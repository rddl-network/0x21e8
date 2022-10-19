# 0x21e8

The 0x21e8 service is usually installed and executed on RDDL compatible hardware wallets.
The current version runs with a software-based keystore. Production based versions will use keystores based on secure elements.

**WARNING** use this code only for demonstrational purposes. Production code must not rely on this service.


## Prepare the Environment
```bash
### For a RPI, ignore the errors with zenroom
bash install.sh
pipenv shell

### For a x86 machine with poetry
curl -sSL https://install.python-poetry.org | python3 -   # instals poetry
poetry install
poetry shell

### For a x86 machine with pipenv
pipenv install
pipenv shell
```

## Service Configuration
The service needs the folloing configurations:
* RDDL network planetmint services (RESTFul)
* RDDL network liquid services (RPC)
    * RPC URL
    * RPC port
    * RPC user
    * RPC password
* web3storage token to store data


## Service Execution
```bash
cd 0x21e8 # that's the folder where main.py is located within
uvicorn --log-level debug --reload main:app
```

## Service deployment

In order to deploy the service within an production environment adjust the user and groupnames if needed and execute the follwoing commands:

```bash
sudo cp 0x21e8.service /etc/systemd/sytem # that's the folder where main.py is located within
sudo systemctl daemon-reload
sudo systemctl start 0x21e8.service
```

### Current state of Liquid Part:

The liquid transactions are created the following way:

#### Confidential Address Derivation
1. A master key is generated from a mnemonic phrase
2. This key is derived once (1) and a child key is acquired.
3. The child key is used to derive a liquid address.
4. .
5. .
6. .
7. Through various steps a confidential address is created. This address is passed along the private key that was used to create the confidential address. This private key is not used anywhere. Apparently, the address is also not used anywhere.

#### Asset Issuance
1. the `issue_asset` function is called which makes a rpc call in the background. The issue here is the confidential address created before is not used. **where do we use the confidential address ? its not used anywhere else**
2. This part is solely handled by RPC calls. **Is the trusted gw also make rpc calls ? or is it going to delegate this to some other backend service ?**
3. After we are done here, we get some kind of receipt for our transaction which will be used later on.

#### Asset Id Registration
1. The asset id will be registered to our trusted domain. **Is this a one time thing ? Are we going to use the same asset / token for every activity ? As far as i have understood, the asset issuer (r&c) does this only once.**

#### Asset Id Registration on Liquid Network
1. The asset id and the corresponding contract is registered on liquid as the final step. **Is this also done only by (r&c) and done only once ?**


It seems like there is a confusion around creating/issuing an asset and actually distributing it to users. The steps here resemble a one-time asset issuance rather than asset distribution (which is called asset re-issuance. 
Here is the official documentation : https://docs.blockstream.com/liquid/developer-guide/developer-guide-index.html#proof-of-issuance-blockstream-s-liquid-asset-registry.
The trusted gateway should ask for a re-issuance of token and this service should do it. The hw should focus on generating an address (from a mnemonic), post the planetmint tx first get the id from this tx and send it along the issuance request to the service so the service can determine how much token will be issued. Maybe its not like this and the issued asset reprents a NFT on Liquid Network so for every create tx from planet mint there will be another asset issued on Liquid. 
