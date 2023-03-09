
# Overview

This is a project used to build [Hootenanny](https://github.com/ngageoint/hootenanny) using the open source package manager, [Conan](https://conan.io/). One specific use is to provide a Hootenanny build for use by [pyhoot](https://github.com/epochgeo/pyhoot).

# Install

# Modifying Hootenanny

Currently, we're working offline from the hoot repo as we have an older version of the code and aren't running tests locally. Where possible, make conflation related changes to `pyhoot` or your code that consumes `pyhoot`. However, there definitely will be times where its cleanest to make changes directly to hoot. To do do:
* Make the code changes. Then compile and generate the diff:
* `cd hootenanny-conan && make && cd build/hoot && git diff > ../../patches/0.2.64b/hoot.patch && cd ../..`
Then commit the modified diff file. This will ensure your changes are preserved when this project is rebuilt.
