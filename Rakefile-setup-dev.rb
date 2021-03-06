import 'Rakefile.rb'

task :configure_pyenv do
    bash_profile = File.expand_path "~/.bash_profile"

    if not File.readlines(bash_profile).grep(/pyenv init/).any?
        File.open(bash_profile, "a") do |f|
            f.puts 'eval "$(pyenv init -)"'
        end
    end
end

task :install_dev_system_dependencies_mac do
    pkg_dependencies = [
        "pyenv", "xz", "gnuplot --cairo --png"
    ]
    install_system_dependencies_mac pkg_dependencies

    system %{sudo easy_install pip}

    install_gitstats

    install_python $PYTHON_VERSION
    install_python $PYTHON_VERSION_GIT_STATS
end

def refresh_packages
    sh %{pyenv rehash}
end

def install_system_dependencies_mac(packages)
    packages.each do |pkg|
        system "brew install #{pkg}"
    end
end

task :install_dev_python_dependencies_mac do
    switch_to_dev_python_version
    install_pypi_dev_dependencies
    refresh_packages
end

def install_gitstats
    system "git clone --depth 1 git://github.com/hoxu/gitstats.git #{$gitstats_dir}"
    Dir.chdir($gitstats_dir){
        sh %{git pull} 
    }
end

def install_pypi_dev_dependencies
    dev_packages = [
        "pkginit", "nose", "freezegun", "coverage",
        "pylint", "pep8",
        "requests", "python-forecastio", "Flask"
    ]
    sudo_install_pypi_packages dev_packages
end

def sudo_install_pypi_packages(pypi_packages)
    pypi_packages.each do |pkg|
        sh "sudo pip install --upgrade #{pkg}"
    end
end

def install_python(python_version)
    puts "install_python " + python_version
    installed_versions = `pyenv versions`

    if not installed_versions.include? python_version
        sh "pyenv install #{python_version}"
        puts "WARNING: close this shell before proceeding"
    end
end

def switch_to_dev_python_version
    use_python $PYTHON_VERSION
    ensure_python_is $PYTHON_VERSION
end

task :run_debug do
    `python webapp/app.py`
end
