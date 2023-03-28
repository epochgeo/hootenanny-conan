# Install

```
# Launch a CentOS 7 VM with the Vagrantfile in this repo and at least 60GB of disk space and login:
vagrant plugin install vagrant-bindfs
cd pyhoot
vagrant up
vagrant ssh

cd ~

# Set up the hoot repo:
wget https://raw.githubusercontent.com/ngageoint/hootenanny-rpms/30149eb7d26ff69f15a1fa6b52d73e4d048b77a3/scripts/hoot-repo.sh
sudo bash hoot-repo.sh
gpg --import /etc/pki/rpm-gpg/RPM-GPG-KEY-Hoot


# Install deps
sudo yum install -y centos-release-scl && sudo yum update -y
sudo yum -y install epel-release
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
# Add an upgrade version of git for pydoc-markdown with endpoint-repo.
sudo yum install -y git devtoolset-8-gcc devtoolset-8-gcc-c++ v8-devel glpk-devel gtk2-devel re2-devel java-1.8.0-openjdk-devel bzip2-devel readline-devel ncurses-devel sqlite-devel gdbm-devel db4-devel libpcap-devel xz-devel wget gtest gtest-devel dnf htop libpostal libpostal-devel stxxl stxxl-devel nano mlocate libffi-devel pandoc texlive-latex-bin-bin texlive-*.noarch https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm
sudo yum groupinstall -y "Development tools"
sudo yum install -y libfontenc-devel libXaw-devel libXdmcp-devel libXtst-devel libxkbfile-devel libXres-devel libXScrnSaver-devel libXvMC-devel xorg-x11-xtrans-devel xcb-util-wm-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel libXv-devel xcb-util-devel xkeyboard-config-devel
sudo updatedb

# Get pyenv so we can use it in bash_profile
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# modify the profile
# Verify this JVM path for your VM.
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b08-1.el7_9.x86_64/include/linux" >> ~/.bash_profile
echo "PYENV_ROOT=$HOME/.pyenv" >> ~/.bash_profile
echo "export PATH=$PATH:$PYENV_ROOT/bin/" >> ~/.bash_profile
echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
echo "export HOOT_HOME=$HOME/pyhoot/build/" >> ~/.bash_profile
echo "export ICU_DATA=$HOME/pyhoot/build/res" >> ~/.bash_profile
echo "export PROJ_LIB=$HOOT_HOME" >> ~/.bash_profile
echo "source /opt/rh/devtoolset-8/enable" >> ~/.bash_profile
source ~/.bash_profile

# Setup our python version
PYTHON_CONFIGURE_OPTS="--enable-shared --with-pic" pyenv install --force 3.7.14
pyenv global 3.7.14
pyenv versions
pip install --upgrade pip
pip install --upgrade setuptools

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

# By default this isn't necessary, vagrant forward's your local keys to the vagrant host.
# As long as you have github keys registered on the machine you're ssh'ing from, this should
# just work.
# # Example of setting up your ssh keys to clone from git:
# ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C brandon@epochgeo.com
# eval "$(ssh-agent -s)"
# chmod 600 ~/.ssh/id_ed25519.pub
# ssh-add ~/.ssh/id_ed25519
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

# This is the last 1.x version. Moving to 2.x will require several changes.
pip install conan==1.59

# Configure Conan: Unfortunately there is a Conan bug that comes up from time to time regarding 
# SSL verification when pulling dep packages. Add `self._verify_ssl = False` to the constructor 
# of `/home/vagrant/.pyenv/versions/3.7.14/lib/python3.7/site-packages/conans/client/downloaders/file_downloader.py`.

cd ~

# The 'False' turns off SSL verification for the remote. You may need to also turn off 
# SSL verification for conancenter by editing ~/.conan/remotes.json.
conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local False

When done, your ~/.conan/remotes.json should look similar to this:
```
{
 "remotes": [
  {
   "name": "conancenter",
   "url": "https://center.conan.io",
   "verify_ssl": false
  },
  {
   "name": "sintef",
   "url": "https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local",
   "verify_ssl": false
  }
 ]
}
```
# get the customized conan profile
git clone git@github.com:epochgeo/hootenanny-conan.git
cd hootenanny-conan
rm ~/.conan/profiles/default
ln -s `pwd`/hoot_profile ~/.conan/profiles/default

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

cd hootenanny-conan
make
export HOOT_HOME=build/hoot/
cd build/hoot
bin/hoot.bin version
```
