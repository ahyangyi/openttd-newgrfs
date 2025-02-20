Ahyangyi's OpenTTD NewGRFs
==========================

![Unit tests](https://github.com/ahyangyi/openttd-newgrfs/actions/workflows/unit-tests.yml/badge.svg)
![Docs](https://github.com/ahyangyi/openttd-newgrfs/actions/workflows/jekyll-gh-pages.yml/badge.svg)

This repo contains the source code for Ahyangyi’s NewGRFs.

A monorepo is used to increase the chance of code sharing. The possibility of refactoring this repo into multiple smaller ones remains, but it is too early to worry about that.

# Building
## Preparation
This depends on an up-to-date version of grf-py. When in doubt, use the SHA1 specified in `requirements.txt`, which is known to work.

Install the Go dependencies with `./install-go-dependencies.sh`. Then add `gopath/bin` to your `PATH` variable.

## Make
After installing dependencies, run `make` to get the newGRFs. Read the makefile to find other options.

# NewGRFs
The documentation of the main branch of this repository is available as [Github Docs](https://ahyangyi.github.io/openttd-newgrfs/).

I try to automate this process as much as possible, so that the docs is always up to date.

Some of the NewGRFs are in very early stages of development, hence the lack of documentation is a feature: there is simply nothing to document.

# Licensing
The released newGRFs will be GPLv2. Everything created by me (that is, anything not in a path containing `third_party`) will be licensed GPLv2+.

Warning: only released versions are guaranteed to contain only GPLv2 compatible stuff, some development versions might use third party files in a way that’s not releasable at all. I allow this situation to happen because code development and graphics development don’t happen simultaneously, and sometimes I need to use incompatible material to get things working first.

# Contributing
Contribution is welcome; contributed code must also be licensed GPLv2+.

If a subproject has more than one contributors, I will change its name to a recursive acronym. For example, "Ahyangyi’s Road Vehicles" becomes "ARV Road Vehicles".

# Other NewGRFs I Make
**China Set: Stations - Wuhu** used to belong to this repo, and the older releases are still listed here. However, it is now moved to a [new place](https://github.com/OpenTTD-China-Set/China-Set-Stations-Wuhu).

I also created a Finnish town name NewGRF, which is available [here](https://github.com/ahyangyi/openttd-finnish-town-names).
