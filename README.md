
# Install

## BDW 9/22/22

Launch CentOS 7 VM and login:
```
vagrant plugin install vagrant-bindfs
cd pyhoot
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
sudo yum -y install epel-release
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel gtk2-devel re2-devel java-1.8.0-openjdk-devel bzip2-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel libpcap-devel xz-devel wget gtest gtest-devel dnf htop libpostal libpostal-devel stxxl stxxl-devel nano mlocate
sudo yum groupinstall -y "Development tools"
sudo dnf install -y libfontenc-devel libXaw-devel libXdmcp-devel libXtst-devel libxkbfile-devel libXres-devel libXScrnSaver-devel libXvMC-devel xorg-x11-xtrans-devel xcb-util-wm-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel libXv-devel xcb-util-devel xkeyboard-config-devel
sudo updatedb
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

How I like to configure git:
```
git config --global user.name "My Name"
git config --global user.email my@email.com
git config --global core.autocrlf input
git config --global branch.autosetuprebase always
git config --global branch.master.rebase true
git config --global core.editor nano
git config --global color.ui true
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

Install hoot conan and custom built deps:
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

cd conan-libphonenumber
make
cd ..

cd conan-libnode
make
cd ..

cd hootenanny-conan
make
export HOOT_HOME=build/hoot/
cd build/hoot
bin/hoot.bin version
```

## Development Flow

https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html
