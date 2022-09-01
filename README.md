
# Install

## Original CentOS 7

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

```
rm -rf tmp/source tmp/build
conan source . --source-folder=tmp/source
# we are rebuilding protbuf b/c the conan center bindings are too new for centos7.
conan install . --install-folder=tmp/build -s compiler.version=9 --build protobuf
conan build . --source-folder=tmp/source --build-folder=tmp/build
conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package
conan export-pkg . test/debug -f --source-folder=tmp/source --build-folder=tmp/build
```

When you're ready for integration testing:

```
conan create . test/debug -s compiler.version=9 --build protobuf
```

## BDW CentOS 7 Tested Install (WIP)

Launch VM and login:
```
cd
vagrant plugin install vagrant-bindfs
vagrant up (had to disable nfs)
vagrant ssh
```

Install deps:
```
# need epel for gtest
sudo yum -y install epel-release
sudo yum repolist
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
# These cause problems when v8-devel is installed
sudo yum remove nodejs nodejs-devel
sudo yum install -y centos-release-scl && sudo yum update -y
sudo yum install gcc zlib-devel bzip2-devel openssl-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel expat-devel libpcap-devel xz-devel pcre-devel gtest gtest-devel git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel nodejs-devel gtk2-devel glpk-devel re2-devel java-1.8.0-openjdk-devel
# Start using the gcc 8 tools, you'll have to do this each time you start a new shell
source /opt/rh/devtoolset-8/enable

# libphonenumber won't compile with the gcc that comes with devtoolset-8 for some reason
wget https://ftp.gnu.org/gnu/gcc/gcc-12.2.0/gcc-12.2.0.tar.gz
tar zxf gcc-12.2.0.tar.gz
cd gcc-12.2.0
./contrib/download_prerequisites
./configure --disable-multilib --enable-languages=c,c++
make
sudo make install
export LD_LIBRARY_PATH=/usr/local/lib64

# conan requires a later version of cmake
sudo yum remove cmake
wget https://cmake.org/files/v3.24/cmake-3.24.1.tar.gz
tar zxvf cmake-3.*.tar.gz
cd cmake-3.*
./bootstrap --prefix=/usr/local
make -j$(nproc)
sudo make install
cmake --version

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
# The conan that comes by default was too early of a version for one of the hoot conan deps:
pip install --upgrade pip
git clone https://github.com/conan-io/conan.git conan
cd conan && sudo pip install -e .
```

Install hoot conan deps:
```
cd ~

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
cd..
```

Install hoot conan:
```
rm -rf tmp/source tmp/build
conan source . --source-folder=tmp/source
# we are rebuilding protbuf b/c the conan center bindings are too new for centos7.
conan install . --install-folder=tmp/build -s compiler.version=9 --build protobuf
conan build . --source-folder=tmp/source --build-folder=tmp/build
conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package
conan export-pkg . test/debug -f --source-folder=tmp/source --build-folder=tmp/build
```

Integration testing:
```
conan create . test/debug -s compiler.version=9 --build protobuf
```
