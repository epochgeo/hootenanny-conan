
# Install

```
# Launch a CentOS 7 VM with the Vagrantfile in this repo and at least 60GB of disk space and login:
vagrant plugin install vagrant-bindfs
cd pyhoot
vagrant up
vagrant ssh

cd ~

# Set up the hoot repo:
wget https://github.com/ngageoint/hootenanny-rpms/blob/30149eb7d26ff69f15a1fa6b52d73e4d048b77a3/scripts/hoot-repo.sh
./hoot-repo.sh
gpg --import /etc/pki/rpm-gpg/RPM-GPG-KEY-Hoot


# Install deps
sudo yum install -y centos-release-scl && sudo yum update -y
sudo yum -y install epel-release
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
# Add an upgrade version of git for pydoc-markdown with endpoint-repo.
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel gtk2-devel re2-devel java-1.8.0-openjdk-devel bzip2-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel libpcap-devel xz-devel wget gtest gtest-devel dnf htop libpostal libpostal-devel stxxl stxxl-devel nano mlocate libffi-devel pandoc texlive-latex-bin-bin texlive-*.noarch https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm
sudo yum groupinstall -y "Development tools"
sudo dnf install -y libfontenc-devel libXaw-devel libXdmcp-devel libXtst-devel libxkbfile-devel libXres-devel libXScrnSaver-devel libXvMC-devel xorg-x11-xtrans-devel xcb-util-wm-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel libXv-devel xcb-util-devel xkeyboard-config-devel
sudo updatedb

# modify the profile
# Verify this JVM path for your VM.
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b08-1.el7_9.x86_64/include/linux" >> ~/.bash_profile
echo "PYENV_ROOT=$HOME/.pyenv" >> ~/.bash_profile
echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
echo "HOOT_HOME=$HOME/pyhoot/build/" >> ~/.bash_profile
echo "ICU_DATA=$HOME/pyhoot/build/res" >> ~/.bash_profile
echo "PROJ_LIB=$HOOT_HOME" >> ~/.bash_profile
echo "/opt/rh/devtoolset-8/enable" >> ~/.bash_profile
source ~/.bash_profile

# The version of conan used requires a later version of cmake:
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
cd ~
rm -f cmake-3.24.1.tar.gz

# # Example of setting up your ssh keys to clone from git:
# ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C brandon@epochgeo.com
# eval "$(ssh-agent -s)"
# chmod 600 ~/.ssh/id_ed25519.pub
# ssh-add ~/.ssh/id_ed25519.pub
# # Now add the public key contents to your github accounts.
# cat ~/.ssh/id_ed25519.pub

# # One way to configure git:
# git config --global user.name "My Name"
# git config --global user.email my@email.com
# git config --global core.autocrlf input
# git config --global branch.autosetuprebase always
# git config --global branch.master.rebase true
# git config --global core.editor nano
# git config --global color.ui true

# Set up Python:
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
PYTHON_CONFIGURE_OPTS="--enable-shared --with-pic" pyenv install --force 3.7.14
pyenv global 3.7.14
pyenv versions
pip install --upgrade pip
pip install --upgrade setuptools

# This is the last 1.x version. Moving to 2.x will require several changes.
pip install conan==1.59

# Configure Conan: Unfortunately there is a Conan bug that comes up from time to time regarding 
# SSL verification when pulling dep packages. Add `self._verify_ssl = False` to the constructor 
# of `/home/vagrant/.pyenv/versions/3.7.14/lib/python3.7/site-packages/conans/client/downloaders/file_downloader.py`.

cd ~

# The '-f False' turns off SSL verification for the remote. You may need to also turn off 
# SSL verification for conancenter by editing ~/.conan/remotes.json.
conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local -f False

git clone git@github.com:epochgeo/liboauthcpp-conan.git
cd liboauthcpp-conan
make
cd ..

git clone git@github.com:epochgeo/conan-libphonenumber.git
cd conan-libphonenumber
make
cd ..

git clone git@github.com:epochgeo/conan-libnode.git
cd conan-libnode
make
cd ..

git clone git@github.com:epochgeo/hootenanny-conan.git
cd hootenanny-conan
ln -s `pwd`/hoot_profile ~/.conan/profiles/default
make
export HOOT_HOME=build/hoot/
cd build/hoot
bin/hoot.bin version
```

# Modifying Hootenanny

Currently, we're working offline from the hoot repo as we have an older version of the code and aren't running tests locally. Where possible, make conflation related changes to `pyhoot` or your code that consumes `pyhoot`. However, there definitely will be times where its cleanest to make changes directly to hoot. To do do:
* Make the code changes. Then compile and generate the diff:
* `cd hootenanny-conand && make && cd build/hoot && git diff > ../../patches/0.2.64b/hoot.patch && cd ../..`
This will ensure your changes are preserved when this project is rebuilt.
