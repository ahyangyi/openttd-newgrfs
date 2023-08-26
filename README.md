Ahyangyi's OpenTTD NewGRFs
==========================

This repo contains the source code for Ahyangyi’s NewGRFs.
A monorepo is used to increase the chance of code sharing. The possibility of refactoring this repo into multiple smaller ones remains, but it is too early to worry about that.

# Building
## Preparation
This depends on an up-to-date version of grf-py.

Install the Go dependencies with `./install-go-dependencies.sh`. Then add `gopath/bin` to your `PATH` variable.

## Make
After installing dependencies, run `make` to get the newGRFs.

# NewGRFs

As of now, this repo contains the following sub-projects:

## Ahyangyi's Road Vehicles
### Dovemere
A generic vehicle set loosely based on vehicles in China, especially those used in [Wuhu](https://en.wikipedia.org/wiki/Wuhu).

## Ahyangyi's Extended Generic Industry Set

# Licensing
The released newGRFs will be GPLv2. Everything created by me (that is, anything not in a path containing `third_party`) will be licensed GPLv2+.

# Contributing
Contribution is welcome; contributed code must also be licensed GPLv2+.

If signicant contribution is made to a NewGRF that begins with `Ahyangyi's`, I will change it to a recursive acronym. For example, "Ahyangyi’s Road Vehicles" becomes "ARV Road Vehicles".
