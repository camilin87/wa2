Weather Alerts 2.0
================

The comprehensive project for the Weather Alerts platform

Development Dependencies
------------------------
Development machines should have these
- git
- xquartz
- homebrew

> sh setup-dev.sh
> rake -f Rakefile-setup-dev.rb install_dev_system_dependencies_mac
> rake -f Rakefile-setup-dev.rb install_dev_python_dependencies_mac

Deployment Dependencies
-----------------------
> cd ~ && wget -q https://raw.githubusercontent.com/camilin87/wa2-setup/master/setup-wa2-prod.sh -O setup-wa2-prod.sh && sh setup-wa2-prod.sh feature/disable-http && cd wa2
> cd ~/wa2 && rake -f Rakefile-prod.rb install_prod_dependencies
> cd ~/wa2/test_integration/ && rake staging && rake staging_ssl && cd ..

Production Deployment Additional Steps
--------------------------------------
> cd ~/wa2 && rake -f Rakefile-prod.rb install_prod_ssl     # TODO
> cd ~/wa2 && rake -f Rakefile-prod.rb disable_http
> cd ~/wa2/test_integration/ && rake production && cd ..
> cd ~/wa2 && rake -f Rakefile-prod.rb disable_debug

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
