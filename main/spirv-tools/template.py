# update and rebuild shaderc when updating
# update vulkan-validationlayers on next release
pkgname = "spirv-tools"
pkgver = "1.3.268.0"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DSPIRV_SKIP_TESTS=ON",
    "-DSPIRV_WERROR=OFF",
    f"-DSPIRV-Headers_SOURCE_DIR={self.profile().sysroot / 'usr'}",
]
hostmakedepends = ["cmake", "ninja", "pkgconf", "python"]
makedepends = ["spirv-headers"]
pkgdesc = "API and commands for processing SPIR-V modules"
maintainer = "q66 <q66@chimera-linux.org>"
license = "Apache-2.0"
url = "https://github.com/KhronosGroup/SPIRV-Tools"
source = f"{url}/archive/vulkan-sdk-{pkgver}.tar.gz"
sha256 = "4c19fdcffb5fe8ef8dc93d7a65ae78b64edc7a5688893ee381c57f70be77deaf"
hardening = ["!cfi"]  # TODO
# needs gtest
options = ["!check"]


@subpackage("spirv-tools-devel-static")
def _static(self):
    self.depends = []
    self.install_if = []

    return ["usr/lib/*.a"]


@subpackage("libspirv-tools-shared")
def _shared(self):
    self.pkgdesc = f"{pkgdesc} (shared library)"

    return ["usr/lib/*.so"]


@subpackage("spirv-tools-devel")
def _devel(self):
    self.depends += [
        f"{pkgname}={pkgver}-r{pkgrel}",
        f"{pkgname}-devel-static={pkgver}-r{pkgrel}",
        f"lib{pkgname}-shared={pkgver}-r{pkgrel}",
    ]

    return self.default_devel()
