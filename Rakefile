task :default => [:all]

$basedir = File.expand_path "."
$gitstats_dir = File.join($basedir, ".git-stats-src/")
$gitstats_path = File.join($gitstats_dir, "gitstats")
$PYTHON_VERSION = "3.4.0"
$PYTHON_VERSION_GIT_STATS = "2.7.6"

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
    system "git clone --depth 1 git://github.com/hoxu/gitstats.git #{$gitstats_dir}"
    Dir.chdir($gitstats_dir){
        sh %{git pull} 
    }
end

def configure_python_version
    install_python $PYTHON_VERSION
    install_python $PYTHON_VERSION_GIT_STATS
    refresh_packages
end

def install_python(python_version)
    puts "install_python" + python_version
    system "yes N | pyenv install #{python_version}"
end

def switch_to_dev_python_version
    use_python $PYTHON_VERSION
end

def switch_to_git_stats_python_version
    use_python $PYTHON_VERSION_GIT_STATS
end

def use_python(python_version)
    puts "use_python" + python_version
    sh "pyenv local #{python_version}"
end

def install_pypi_dev_dependencies
    pypi_packages = [
        "nose", "mock", "freezegun", "coverage",
        "pylint", "pep8", "python-forecastio"
    ]
    pypi_packages.each do |pkg|
        sh "sudo pip install --upgrade #{pkg}"
    end 
end

def refresh_packages
    puts "refresh_packages"
end