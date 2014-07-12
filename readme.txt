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
> rake install_dev_dependencies_mac

Deployment Dependencies
-----------------------
> cd ~ && wget -q https://raw.githubusercontent.com/camilin87/wa2-setup/master/setup-wa2-prod.sh -O setup-wa2-prod.sh && sh setup-wa2-prod.sh feature/wf-bottle && cd wa2 # Make sure to open a new terminal after the first execution finishes.
> cd ~/wa2 && rake install_prod_dependencies

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
