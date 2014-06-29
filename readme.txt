Weather Alerts 2.0
================

The comprehensive project for the Weather Alerts platform

Development Dependencies
------------------------
Development machines should have these
- git
- ruby
- homebrew

/*
Configure pyenv. Make sure to open a new terminal after the execution finishes
> make configure-pyenv

Install python packages dependencies
> make install-dev-dependencies-mac

Install sourceforge dependencies
- gnuplot # Alternative gnuplot can be installed using homebrew >brew install gnuplot --cairo --png
- gitstats
*/

Deployment Dependencies
-----------------------
- not deployed yet

Coding Standards
----------------
- camel_case_variables
- PascalCase for class names
- Strict TDD should be enforced
- Use Double quotes for strings and dictionaries
- No comments
- Prefer 'from module1 import class1' vs 'import module1'

Unit Tests and Reports
----------------------
Makefile contains all the necessary documentation on how to execute unit tests and generate reports.
