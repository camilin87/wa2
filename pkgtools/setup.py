from os import path
pkg_dir_path = path.dirname(path.realpath(__file__))
pkg_dir = path.basename(pkg_dir_path)

from distutils.core import setup

setup(
    name = pkg_dir,
    version = "0.1",
    author = "CASH Productions",
    author_email = "support@cash-productions.com",
    description = ("Generic __index__.py generator"),
    long_description = """
The contents of your __init__.py files should be:

from pkgtools.modules.modules import load_modules
load_modules(__file__)

""",
    license = "Proprietary",
    keywords = "package module loader",
    packages = [pkg_dir + ".modules"]
)
