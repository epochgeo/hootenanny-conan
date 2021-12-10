from pprint import pprint

from conans import ConanFile, CMake
#from conan.tools.cmake import CMakeToolchain, CMake
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

    build_policy = ["missing", "cascade"]

    exports = f"patches/{version}/*"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {
        "shared": True,
        "fPIC": True,
        "qt:shared": False,
        "coinglpk:shared": False,
        "libphonenumber:shared": False,
        "qt:with_icu": False,
        "qt:with_glib": False,
        "qt:gui": True,
        "qt:qt3d": False,
        "qt:opengl": "no",
        "qt:widgets": False,
        "qt:with_sqlite3": False,
        "qt:with_pq": False,
        "qt:with_mysql": False,
        "gdal:shared": False,
        "boost:shared": False,
        "opencv:shared": False,
        "openssl:shared": False,
        "protobuf:shared": False,
        "libtiff:shared": False,
        "liboauthcpp:shared": False,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "hoot/*"

    requires = [
        "boost/1.71.0",
        "coinglpk/[>=4.65]@sintef/stable",
        "gdal/3.2.1",
        "opencv/2.4.13.7",
        "openssl/1.1.1l",
        "protobuf/3.15.5",
        "qt/5.15.2",
        # explicity require libtiff to avoid a conflict in gdal/opencv
        "libtiff/4.3.0",
        "liboauthcpp/0.1@test/debug",
        "libphonenumber/[>=8.12.27]@test/debug",
    ]

    generators = "cmake_find_package", "cmake", "qt"
    #generators = "cmake"
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

    #def generate(self):
    #    tc = CMakeToolchain(self)
    #    tc.generate()

    def build(self):

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
            (f"patches/{self.version}/HootEnv.sh", "scripts/"),
            (f"patches/{self.version}/hoot", "scripts/"),
        ]

        self.run("mkdir -p %s/hoot/build/" % (self.source_folder))

        for copy_from, copy_to in copy_me:
            self.run("cp -u %s/%s %s/hoot/%s" % (self.recipe_folder, copy_from, 
                self.source_folder, copy_to))

        #self.run(f"cp {self.build_folder}/conanbuildinfo.cmake {self.source_folder}/hoot/")

        cmake = CMake(self)
        cmake.parallel = 8
        cmake.configure()
        cmake.build()
        #self.run(f"cd {self.build_folder}; cmake {self.source_folder}")
        #self.run(f"cd {self.build_folder}; make -j`nproc`")
        #self.run("cmake . --build")
        #self.run("make -j`nproc`")

    def package(self):
        #self.run("cmake --install " + self.source_folder)
        self.copy("*", dst="bin", src="hoot/bin/")
        self.copy("*", dst="conf", src="hoot/conf/")
        self.copy("*", dst="rules", src="hoot/rules/")
        self.copy("HootEnv.sh", dst="bin", src="hoot/scripts/")
        self.copy("RunHoot.sh", dst="bin", src="hoot/scripts/")
        self.copy("*.h", dst="include", src="hoot/hoot-core/src/main/cpp/")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["HootCore"]
