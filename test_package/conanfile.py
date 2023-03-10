from conans import ConanFile, CMake, tools
import os

class LibmemcachedTestConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake", "cmake_find_package_multi"



    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            cmd = os.path.join("bin", "PackageTest")
            self.run(cmd, env="conanrun")
