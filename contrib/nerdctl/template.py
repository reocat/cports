pkgname = "nerdctl"
pkgver = "1.7.0"
pkgrel = 1
build_style = "go"
make_build_args = ["./cmd/nerdctl"]
hostmakedepends = ["go"]
depends = ["containerd", "iptables"]
pkgdesc = "Containerd CLI"
maintainer = "psykose <alice@ayaya.dev>"
license = "Apache-2.0"
url = "https://github.com/containerd/nerdctl"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "10e573a3a0422314cf2989aea6045f95275f40f5489d980203a1039f731de501"
# objcopy fails to split on ppc
# can't run tests inside namespaces
options = ["!debug", "!check"]


def post_build(self):
    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"nerdctl.{shell}", "w") as f:
            self.do(
                self.chroot_cwd / self.make_dir / "nerdctl",
                "completion",
                shell,
                stdout=f,
            )


def post_install(self):
    self.install_service(self.files_path / "containerd.user")
    self.install_bin(
        "extras/rootless/containerd-rootless.sh", name="containerd-rootless"
    )
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"nerdctl.{shell}", shell)


@subpackage("containerd-rootless")
def _rless(self):
    self.pkgdesc = "Rootless containerd support"
    self.depends = [
        "containerd",
        "rootlesskit",
        "slirp4netns",
    ]

    return [
        "etc/dinit.d/user",
        "usr/bin/containerd-rootless",
    ]
