task :default => [:all]

task :configure_pyenv do
    bash_profile = File.expand_path "~/.bash_profile"
    if not File.readlines(bash_profile).grep(/pyenv init/).any?
        File.open(bash_profile, "a") do |f|
            f.puts 'eval "$(pyenv init -)"'
        end
    end
end

task :install_dev_dependencies_mac do
    system %{brew install pyenv}
    system %{brew install xz}
    system %{brew install gnuplot --cairo --png}
    system %{sudo easy_install pip}

    Rake::Task["install_dev_dependencies"].execute
end

task :install_dev_dependencies do
    install_gitstats
    configure_python_version
    switch_to_dev_python_version
    install_pypi_dev_dependencies
    refresh_packages
end

def install_gitstats
    puts "install_gitstats"
end

def configure_python_version
    puts "configure_python_version"
end

def switch_to_dev_python_version
    puts "switch_to_dev_python_version"
end

def install_pypi_dev_dependencies
    puts "install_pypi_dev_dependencies"
end

def refresh_packages
    puts "refresh_packages"
end