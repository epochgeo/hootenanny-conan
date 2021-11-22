
## Install

```
sudo apt install valac-bin valac-0.48-vapi
```

## Development Flow

https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html



```
mkdir build
cd build
rm -rf tmp
conan source . --source-folder=tmp/source
conan install . --install-folder=tmp/build
conan build . --source-folder=tmp/source --build-folder=tmp/build
conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package
conan export-pkg . test/debug --source-folder=tmp/source --build-folder=tmp/build --profile=myprofile
```

When you're ready for integration testing:

```
mkdir build
cd build
rm -rf tmp
conan create .. test/debug
```
