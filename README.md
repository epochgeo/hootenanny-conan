
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
vagrant up (had to disable nfs in Vagrantfile)
vagrant ssh
```

Add Hootenanny repo to `/etc/yum.repos.d/hoot.repo`:
```
[hoot-deps]
name = Hootenanny Dependencies
baseurl = https://hoot-repo.s3.amazonaws.com/el7/deps/stable
enable = 1
gpgcheck = 1
repo_gpgcheck = 1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Hoot
```

Install deps:
```
sudo yum install -y centos-release-scl && sudo yum update -y
# need epel for gtest required by later version of cmake installed later on
sudo yum -y install epel-release
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
# These cause problems when v8-devel is installed.
#sudo yum remove nodejs nodejs-devel
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel gtk2-devel re2-devel java-1.8.0-openjdk-devel bzip2-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel libpcap-devel xz-devel wget gtest dnf htop libpostal stxxl nano
# Now add them back.
#sudo yum install -y nodejs nodejs-devel
sudo yum groupinstall -y "Development tools"
sudo dnf install -y libfontenc-devel libXaw-devel libXdmcp-devel libXtst-devel libxkbfile-devel libXres-devel libXScrnSaver-devel libXvMC-devel xorg-x11-xtrans-devel xcb-util-wm-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel libXv-devel xcb-util-devel xkeyboard-config-devel
# Start using the gcc 8 tools, YOU'LL HAVE TO DO THIS EACH TIME YOU START A NEW SHELL
source /opt/rh/devtoolset-8/enable
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
# Now add the public key contents to your github accounts.
cat ~/.ssh/id_ed25519.pub
```

JNI:
```
find / -name jni_md.h 2> /dev/null
# TODO: make this permanent
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.342.b07-1.el7_9.x86_64/include/linux/
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
```

Set up Python env:
```
source ~/.bash_profile
pyenv install 3.6.8
pyenv global 3.6.8
pyenv versions
```

Install Conan:
```
pip install conan
```

Install hoot conan and deps:
```
cd ~

conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local

source /opt/rh/devtoolset-8/enable

git clone https://github.com/epochgeo/liboauthcpp-conan.git
git clone https://github.com/epochgeo/conan-libnode.git
git clone https://github.com/epochgeo/conan-libphonenumber.git
git clone https://github.com/epochgeo/hootenanny-conan.git
cd hootenanny-conan
rm ~/.conan/profiles/default
ln -s `pwd`/hoot_profile ~/.conan/profiles/default

cd ..

cd liboauthcpp-conan
make
cd ..

cd conan-libnode
make
cd ..

cd conan-libphonenumber
make
cd ..

cd hootenanny-conan
make
cd build/hoot
bin/hoot.bin version
```
