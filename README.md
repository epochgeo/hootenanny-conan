
# Install

## JRS January 2022

### Ubuntu 20.04

```
sudo apt install valac-bin valac-0.48-vapi
```

### CentOS 7

Add external conan deps:

```
conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
```

```
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
sudo yum install -y centos-release-scl && sudo yum update -y
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ libgtk2-devel v8-devel \
    glpk-devel nodejs-devel gtk2-devel glpk-devel python27-devel re2-devel java-1.8.0-openjdk-devel
# Start using the gcc 8 tools, you'll have to do this each time you start a new shell
source /opt/rh/devtoolset-8/enable
```

Ugh. Use the install steps for STXXL here:
https://github.com/ngageoint/hootenanny/blob/master/scripts/util/Centos7_only_core.sh#L194

### Development Flow

https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

## BDW 9/7/22

Launch CentOS 7 VM and login:
```
cd
vagrant plugin install vagrant-bindfs
vagrant up (had to disable nfs)
vagrant ssh
```

Install deps:
```
sudo yum install -y centos-release-scl && sudo yum update -y
# need epel for gtest required by later version of cmake installed later on
sudo yum -y install epel-release
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
# These cause problems when v8-devel is installed.
sudo yum remove nodejs nodejs-devel
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel gtk2-devel re2-devel java-1.8.0-openjdk-devel bzip2-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel libpcap-devel xz-devel wget gtest dnf htop
sudo yum groupinstall "Development tools"
sudo dnf install -y libfontenc-devel libXaw-devel libXdmcp-devel libXtst-devel libxkbfile-devel libXres-devel libXScrnSaver-devel libXvMC-devel xorg-x11-xtrans-devel xcb-util-wm-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel libXv-devel xcb-util-devel xkeyboard-config-devel
# Start using the gcc 8 tools, YOU'LL HAVE TO DO THIS EACH TIME YOU START A NEW SHELL
source /opt/rh/devtoolset-8/enable
```

libphonenumber won't compile with the gcc that comes with devtoolset-8 for some reason. Installing a later version of gcc adds some needed ABI later header files. We're not actually going to use this version of gcc, as we'll still use gcc 8 installed by dev-toolset 8. Compiling gcc is a bear, so simply installing a version late enough to have the appropriate ABI version would be far simpler, although I haven't figured out yet how to do that on CentOS 7:
```
wget https://ftp.gnu.org/gnu/gcc/gcc-12.2.0/gcc-12.2.0.tar.gz
tar zxf gcc-12.2.0.tar.gz
cd gcc-12.2.0
./contrib/download_prerequisites
./configure --disable-multilib --enable-languages=c,c++
make
sudo make install
```

The version of conan used requires a later version of cmake:
```
sudo yum remove cmake
wget https://cmake.org/files/v3.24/cmake-3.24.1.tar.gz
tar zxvf cmake-3.*.tar.gz
cd cmake-3.*
./bootstrap --prefix=/usr/local
make -j$(nproc)
sudo make install
cd /usr/bin
sudo ln -s /usr/local/bin/cmake cmake
cmake --version
```

Example of setting up your ssh keys to clone from git (in case you forgot):
```
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C brandon@epochgeo.com
eval "$(ssh-agent -s)"
chmod 600 ~/.ssh/id_ed25519.pub
ssh-add ~/.ssh/id_ed25519.pub
```

STXXL:
```
git clone http://github.com/stxxl/stxxl.git stxxl
cd stxxl
git checkout -q tags/1.3.1
make config_gnu
echo "STXXL_ROOT	=`pwd`" > make.settings.local
echo "ENABLE_SHARED     = yes" >> make.settings.local
echo "COMPILER_GCC      = g++ -std=c++0x" >> make.settings.local
# Total hack because 1.3.1 doesn't compile right on CentOS7
sed -i 's/#include <sys\/mman.h>/#include <sys\/mman.h>\n#include <unistd.h>/g' ./utils/mlock.cpp
make -s library_g++
#### Isn't easy, no 'make install'
sudo install -p -D -m 0755 lib/libstxxl.so /usr/local/lib/libstxxl.so.1.3.1
sudo mkdir -p /usr/local/include
sudo cp -pr include/* /usr/local/include/
pushd .
cd /usr/local/lib
sudo ln -s libstxxl.so.1.3.1 libstxxl.so.1
sudo ln -s libstxxl.so.1.3.1 libstxxl.so
popd
```

Get pyenv:
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Add to ~/.bash_profile:
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
```

Set up Python env:
```
pyenv install 3.6.8
pyenv versions
pyenv global 3.6.8
```

Install Conan:
```
pip install conan
```

Install hoot conan and deps:
```
cd ~

conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local

git clone git@github.com:epochgeo/conan-libnode.git
cd conan-libnode
make
cd ..

git clone git@github.com:epochgeo/liboauthcpp-conan.git
cd liboauthcpp-conan
cp /home/vagrant/liboauthcpp-conan/build/generators/CMakePresets.json /home/vagrant/liboauthcpp-conan/build/build/generators/
make
cd ..

git clone git@github.com:epochgeo/conan-libphonenumber.git
cd conan-libphonenumber
make
cd ..

# TODO: still working on this part...get qt errors that it can't find ICU or psql
git clone git@github.com:epochgeo/hootenanny-conan.git
cd hootenanny-conan
make
cd ..
```

At certain times, I would have to add `--build=missing` to the install command in the `Makefile` when building some of the above...don't completely understand why. You can also clean out conan deps from `~/.conan/data`, which is helpful at times.

https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

Integration testing:
```
conan create . test/debug -s compiler.version=9 --build protobuf
```
