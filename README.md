
## Install

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
https://github.com/ngageoint/hootenanny/blob/v0.2.71/scripts/util/Centos7_only_core.sh#L196


## Development Flow

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
