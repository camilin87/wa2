Weather Alerts 2.0
================

The comprehensive project for the Weather Alerts platform

Development Dependencies
------------------------
Development machines should have these
- git
- xquartz
- homebrew

> sh setup-dev.sh # Make sure to open a new terminal after the execution finishes.
> ant install-dev-dependencies-mac

Install python packages dependencies
> ant install-dev-dependencies-mac

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
Rakefile contains all the necessary documentation on how to execute unit tests and generate reports.
