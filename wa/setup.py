def _log(obj):
    print(obj)

from os import path
pkg_dir_path = path.dirname(path.realpath(__file__))
pkg_dir = path.basename(pkg_dir_path)
_log(pkg_dir_path)
_log(pkg_dir)

from os import listdir
sub_pkgs = []
for dir_entry in listdir(pkg_dir_path):
    full_path = path.join(pkg_dir_path, dir_entry)
    if path.isdir(full_path):
        init_path = path.join(full_path, "__init__.py")
        if path.isfile(init_path):
            sub_pkgs.append(pkg_dir + "." + dir_entry)
_log(sub_pkgs)

from distutils.core import setup

setup(
    name = "wa",
    version = "0.1",
    author = "CASH Productions",
    author_email = "support@cash-productions.com",
    description = ("Wa application"),
    license = "Proprietary",
    keywords = "weather API smart location",
    packages = sub_pkgs
)
