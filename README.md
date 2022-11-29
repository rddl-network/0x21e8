# 0x21e8 RDDL Interaction Service

The 0x21e8 service is usually installed and executed on RDDL compatible hardware wallets (HW-03). The service utilizes the hardware wallet and enables the HW-03 devices to interact with the RDDL network (Planetmint and liquid). 

Besides the pure wallet functionality it works as the core service to launch any RDDL specific use cases:
* storage of (un/encrypted) data (w3storage (IPFS))
* attestation of data
* attestation of machines
* issuing of tokens
* lookup of data
* lookup of tokens
* combination of data & tokens

The current version runs with a software-based keystore. Production based versions will use keystores based on secure elements. Initialization and configuration of the keystores is currently enabled via API. 

The service exposes all features via a RESTFul API. The documentation of the API is exposed via <ip/hostname>/docs.

**WARNING** use this code only for demonstrational purposes. Production code must not rely on this service.


## Prepare the Environment
```bash
### For a RPI, ignore the errors with poetry add  ./external_packages_armv7/zenroom-2.1.0.dev1655293214-cp39-cp39-linux_armv7l.whl
bash install.sh

### For a x86 machine with poetry
curl -sSL https://install.python-poetry.org | python3 -   # installs poetry
poetry install
poetry shell
```

## Service Configuration
The service needs the following configurations:
* RDDL network planetmint services (RESTFul)
* RDDL network liquid services (RPC)
    * RPC URL
    * RPC port
    * RPC user
    * RPC password
* web3storage token to store data

The configuration is set via environment variables such as
* LQD_RPC_PORT
* LQD_RPC_USER
* LQD_RPC_PASSWORD
* LQD_RPC_ENDPOINT
* PLNTMNT_ENDPOINT
* WEB3STORAGE_TOKEN

Alternatively, the variables can be defined within the ```.env``` file of the project. A example ```env.example``` file can be adjusted and copied to ```.env```.

## Service Execution
```bash
uvicorn --log-level debug --reload x21e8.main:app
```

## Service deployment

In order to deploy the service within an production environment adjust the user and group names if needed and execute the following commands:

```bash
sudo cp 0x21e8.service /etc/systemd/system # that's the folder where main.py is located within
sudo systemctl daemon-reload
sudo systemctl enable 0x21e8.service
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
The trusted gateway should ask for a re-issuance of token and this service should do it. The hw should focus on generating an address (from a mnemonic), post the planetmint tx first get the id from this tx and send it along the issuance request to the service so the service can determine how much token will be issued. Maybe its not like this and the issued asset represents a NFT on Liquid Network so for every create tx from planet mint there will be another asset issued on Liquid. 
