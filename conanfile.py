from pprint import pprint

from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake
from conan.tools.files import patch, apply_conandata_patches, rename
from conan.tools.layout import cmake_layout


class HootenannyConan(ConanFile):
    name = "hootenanny"
    version = "0.2.64b"

    # Optional metadata
    license = "MIT License"
    homepage = "https://github.com/ngageoint/hootenanny"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Hootenanny conflates multiple maps into a single seamless map."
    topics = ("oauth")

    exports = f"patches/{version}/*"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "hoot/*"

    requires = [
	"boost/1.71.0",
        "gdal/3.2.1",
        "opencv/2.4.13.7",
        "openssl/1.1.1l",
	"protobuf/3.15.5",
        "qt/5.15.2",
        # explicity require libtiff to avoid a conflict in gdal/opencv
        "libtiff/4.3.0",
        "liboauthcpp/0.1@test/debug",
    ]

    generators = "cmake"
    # scm = {
    #     "type": "git",
    #     "url": "https://github.com/ngageoint/hootenanny",
    #     "subfolder": "hoot"
    # }

    def source(self):
        self.run("git clone https://github.com/ngageoint/hootenanny hoot")
        #self.run("cd %s/hoot; git apply %s/hoot.diff" % (self.source_folder, self.recipe_folder))
        #self.run("cd hoot; git apply ../hoot.diff")
        #patch("hoot.diff")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    # def layout(self):
    #     cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        #cmake = CMake(self)
        #cmake.parallel = True
        #cmake.configure()
        #cmake.build()
        self.run("echo %s" % (self.install_folder))
        self.run("echo %s" % (self.build_folder))
        self.run("echo %s" % (self.recipe_folder))
        self.run("echo %s" % (self.source_folder))
        self.run("echo %s" % (self.package_folder))
        self.run("pwd")
        pprint(self.buildenv_info)
        pprint(self.buildenv)
        print(self.source_folder)
        print(self.build_folder)

        # Apply Patches
        for it in self.conan_data.get("patches", {}).get(self.version, []):
           self.run("echo here; pwd; cd %s/hoot; git apply %s/%s; cd .." % 
                (self.source_folder, self.recipe_folder, it["patch_file"]))

        # Copy extra files
        copy_me = [
            (f"patches/{self.version}/HootConfig.h", "/hoot-core/src/main/cpp/hoot/core/"),
            (f"patches/{self.version}/TgsConfig.h", "/tgs/src/main/cpp/tgs/"),
            (f"patches/{self.version}/VersionDefines.h", "/hoot-core/src/main/cpp/hoot/core/info/"),
            (f"patches/{self.version}/CMakeLists.txt", "/."),
        ]

        self.run("mkdir -p %s/hoot/build/" % (self.source_folder))

        for copy_from, copy_to in copy_me:
            self.run("cp %s/%s %s/hoot/%s" % (self.recipe_folder, copy_from, 
                self.source_folder, copy_to))

        self.run(f"cp {self.build_folder}/conanbuildinfo.cmake {self.source_folder}/hoot/")

        self.run(f"cd {self.build_folder}; cmake {self.source_folder}")
        self.run(f"cd {self.build_folder}; make -j`nproc`")
        #self.run("cmake . --build")
        #self.run("make -j`nproc`")

    def package(self):
        #self.run("cmake --install " + self.source_folder)
        self.copy("*.h", dst="include", src="hoot/hoot-core/src/main/cpp/")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["HootCore"]
