from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps
from conan.tools.build import cross_building
from conans import AutoToolsBuildEnvironment, tools
from conan.tools.layout import basic_layout
from conan.tools.files import apply_conandata_patches, get, copy, export_conandata_patches
import os

#import pydevd_pycharm
#pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)

class LibmemcachedConan(ConanFile):
    name = "libmemcached"
    version = "1.0.18"

    # Optional metadata
    license = "MIT"
    author = "Marek Kwasecki <marek.kwasecki@radpoint.pl>"
    #url = "https://github.com/conan-io/conan-center-index"
    url = "https://github.com/kwach/libmemcached.conan"
    homepage = "https://libmemcached.org/"
    description = """libmemcached is a C client library for interfacing to a memcached server. 
    It has been designed to be light on memory usage, thread safe and to provide full access to server side methods. 
    It also implements several command line tools: memcat, memflush, memrm, memstat, and memslap (for load generation). 
    The library has been designed to allow for different hashing methods on keys, 
    partitioning by keys, and to use consistent hashing for distribution."""
    topics = ("cache", "network", "cloud")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "sasl": [True, False]
    }
    default_options = {"shared": False, "fPIC": True, "sasl": False}

    # def layout(self):
    #     basic_layout(self, src_folder="src")

    #def build_requirements(self):
    #    self.tool_requires("libtool/2.4.6")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
                strip_root=True, destination=self.source_folder)

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")


    def _patch_source(self):
        apply_conandata_patches(self)

    def generate(self):
        yes_no = lambda v: "yes" if v else "no"

        env = VirtualBuildEnv(self)
        env.generate()
        if not cross_building(self):
            env = VirtualRunEnv(self)
            env.generate(scope="build")
        tc = AutotoolsToolchain(self)
        tc.configure_args.append('--disable-dependency-tracking')
        if not self.options.sasl:
            tc.configure_args.append("--disable-sasl")
        #tc.configure_args.append("--enable-shared={}".format({yes_no(self.options.shared)}))
        #tc.configure_args.append("--enable-static={}".format({yes_no(not self.options.shared)}))
        tc.generate()

        AutotoolsDeps(self).generate()

    def build(self):
        self._patch_source()

        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))

        autotools = Autotools(self)
        autotools.install()
        # am = AutoToolsBuildEnvironment(self)
        # am.install(args=[f"DESTDIR={tools.unix_path(self, self.package_folder)}"])
        # fix_apple_shared_install_name(self)

    def package_info(self):
        self.cpp_info.libs = ["memcached"]

