#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "libqrencode"
    version = "4.0.0"
    url = ""
    description = "A fast and compact QR Code encoding library"
    license = "https://github.com/fukuchi/libqrencode/blob/master/COPYING"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    #use static org/channel for libs in conan-center
    #use dynamic org/channel for libs in bincrafters
    requires = "libiconv/1.15@bincrafters/stable", \
        "libpng/1.6.34@bincrafters/stable"

    def source(self):
        source_url = "https://github.com/fukuchi/libqrencode"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False 
        cmake.definitions["BUILD_TOOLS"] = False 
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
