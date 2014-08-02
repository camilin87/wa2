#!/bin/sh

# IMPORTANT: do not add anything else to this file
# once rake is installed everything should be run through it
brew install ruby
yes N | gem install rake
rake -f Rakefile-setup-dev.rb configure_pyenv
