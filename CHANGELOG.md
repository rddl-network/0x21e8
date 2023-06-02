# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.1] - 2023-06-02
### Fixed
- from dict to string: bug fix within machine attestation
- improved buggy error handling of the API


## [0.7.0] - 2023-05-10
### Fixed
- using latest planetmint-aio:latest for testing from now on
- Fixed value conversion bugs of string2dict conversions that happened during the data/asset storage process
### Added
- storage tests to verify that no conversions are done


## [0.6.1] - 2023-05-10
### Removed
- removed wallycore dependency (just relying on the sys installation of libwallycore)

## [0.6.0] - 2023-04-17
### Fixed
- Support for Planetmint 2.4 and script tags
- added versioned releases for 0x21e8 and it's docker image

## [0.4.1] - 2023-04-06
### Added
- Added the capabilities of trading fungible tokens on planetmint


## [0.4.0] - 2023-03-28
### Added
- Wallet endpoint and simple asset transfers for Planetmint
