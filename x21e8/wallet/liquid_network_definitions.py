VER_MAIN_PUBLIC = 0x0488B21E
VER_MAIN_PRIVATE = 0x0488ADE4
VER_TEST_PUBLIC = 0x043587CF
VER_TEST_PRIVATE = 0x04358394


WALLY_WIF_FLAG_COMPRESSED = 0x0  # Corresponding public key compressed */
WALLY_WIF_FLAG_UNCOMPRESSED = 0x1  # Corresponding public key uncompressed */
WALLY_CA_PREFIX_LIQUID = 0x0C  # Liquid v1 confidential address prefix */
WALLY_CA_PREFIX_LIQUID_REGTEST = 0x04  # Liquid v1 confidential address prefix for regtest */
WALLY_CA_PREFIX_LIQUID_TESTNET = 0x17  # Liquid v1 confidential address prefix for testnet */
WALLY_NETWORK_BITCOIN_MAINNET = 0x01  # Bitcoin mainnet */
WALLY_NETWORK_BITCOIN_TESTNET = 0x02  # Bitcoin testnet */
WALLY_NETWORK_LIQUID = 0x03  # Liquid v1 */
WALLY_NETWORK_LIQUID_REGTEST = 0x04  # Liquid v1 regtest */
WALLY_NETWORK_LIQUID_TESTNET = 0x05  # Liquid v1 testnet */
WALLY_ADDRESS_TYPE_P2PKH = 0x01  # P2PKH address ("1...") */
WALLY_ADDRESS_TYPE_P2SH_P2WPKH = 0x02  # P2SH-P2WPKH wrapped SegWit address ("3...") */
WALLY_ADDRESS_TYPE_P2WPKH = 0x04  # P2WPKH native SegWit address ("bc1...)" */
WALLY_ADDRESS_VERSION_P2PKH_MAINNET = 0x00  # P2PKH address on mainnet */
WALLY_ADDRESS_VERSION_P2PKH_TESTNET = 0x6F  # P2PKH address on testnet */
WALLY_ADDRESS_VERSION_P2PKH_LIQUID = 0x39  # P2PKH address on liquid v1 */
WALLY_ADDRESS_VERSION_P2PKH_LIQUID_REGTEST = 0xEB  # P2PKH address on liquid v1 regtest */
WALLY_ADDRESS_VERSION_P2PKH_LIQUID_TESTNET = 0x24  # P2PKH address on liquid v1 testnet */
WALLY_ADDRESS_VERSION_P2SH_MAINNET = 0x05  # P2SH address on mainnet */
WALLY_ADDRESS_VERSION_P2SH_TESTNET = 0xC4  # P2SH address on testnet */
WALLY_ADDRESS_VERSION_P2SH_LIQUID = 0x27  # P2SH address on liquid v1 */
WALLY_ADDRESS_VERSION_P2SH_LIQUID_REGTEST = 0x4B  # P2SH address on liquid v1 regtest */
WALLY_ADDRESS_VERSION_P2SH_LIQUID_TESTNET = 0x13  # P2SH address on liquid v1 testnet */
WALLY_ADDRESS_VERSION_WIF_MAINNET = 0x80  # Wallet Import Format on mainnet */
WALLY_ADDRESS_VERSION_WIF_TESTNET = 0xEF  # Wallet Import Format on testnet */


# define BIP32_PATH_MAX_LEN 255

# /** Indicate that we want to derive a private key in `bip32_key_from_parent` */
BIP32_FLAG_KEY_PRIVATE = 0x0
# /** Indicate that we want to derive a public key in `bip32_key_from_parent` */
BIP32_FLAG_KEY_PUBLIC = 0x1
# /** Indicate that we want to skip hash calculation when deriving a key in `bip32_key_from_parent` */
BIP32_FLAG_SKIP_HASH = 0x2
# /** Indicate that we want the pub tweak to be added to the calculation when deriving a key in `bip32_key_from_parent` */
# /** Only used with elements */
BIP32_FLAG_KEY_TWEAK_SUM = 0x4
# /** Allow a wildcard ``*`` or ``*'``/``*h`` in path string expressions */
BIP32_FLAG_STR_WILDCARD = 0x8
# /** Do not allow a leading ``m``/``M`` or ``/`` in path string expressions */
BIP32_FLAG_STR_BARE = 0x10
