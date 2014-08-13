VERSION = "0.1"

def _log(obj):
    print(obj)

from os import path
_PKG_DIR_PATH = path.dirname(path.realpath(__file__))
_PKG_DIR = path.basename(_PKG_DIR_PATH)
_log(_PKG_DIR_PATH)
_log(_PKG_DIR)

from os import listdir
_SUB_PKGS = []
for dir_entry in listdir(_PKG_DIR_PATH):
    full_path = path.join(_PKG_DIR_PATH, dir_entry)
    if path.isdir(full_path):
        init_path = path.join(full_path, "__init__.py")
        if path.isfile(init_path):
            _SUB_PKGS.append(_PKG_DIR + "." + dir_entry)
_log(_SUB_PKGS)

from distutils.core import setup

setup(
    name=_PKG_DIR,
    version=VERSION,
    author="CASH Productions",
    author_email="support@cash-productions.com",
    description=("Wa application"),
    license="Proprietary",
    keywords="weather API smart location",
    packages=_SUB_PKGS
)
